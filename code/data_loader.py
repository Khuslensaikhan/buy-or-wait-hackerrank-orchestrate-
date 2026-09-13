"""Strict schema parsing and request-scoped retrieval; no prediction labels in Dataset."""
import csv
from dataclasses import dataclass, fields
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Iterable, TypeVar

from models import (Event, ExchangeRate, ImageEvidence, Message, OutputRecord,
                    Payment, PaymentOption, Profile, Request, RequestContext,
                    SpendingChange)

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FIELDS = ('request_id', 'amount_safe_to_pay', 'affordability_status',
                 'recommended_payment_method', 'payment_plan',
                 'earliest_date_for_full_payment', 'spending_changes_needed',
                 'decision_explanation')
REQUEST_FIELDS = tuple(f.name for f in fields(Request))
T = TypeVar('T')
CURRENCIES = frozenset({'INR', 'ZAR', 'IDR', 'USD', 'EUR'})
METHODS = frozenset({'full_payment', 'partial_payment', 'installments'})
REQUEST_TYPES = frozenset({'purchase', 'travel', 'education', 'family_transfer',
                           'debt_repayment', 'investment', 'housing', 'emergency_expense', 'other'})


def read_rows(path: Path, headers: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != headers:
            raise ValueError(f'{path.name}: unexpected headers {reader.fieldnames}')
        result = []
        for line, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'{path.name}:{line}: malformed row')
            result.append({key: value.strip() for key, value in row.items()})
        return result


def money(value: str) -> Decimal:
    number = Decimal(value)
    if not number.is_finite() or number < 0:
        raise ValueError(f'invalid nonnegative money: {value!r}')
    return number


def optional_money(value: str) -> Decimal | None:
    return money(value) if value else None


def optional_date(value: str) -> date | None:
    return date.fromisoformat(value) if value else None


def tokens(value: str) -> frozenset[str]:
    return frozenset(part.strip() for part in value.split('|') if part.strip())


def parse_request(row: dict[str, str]) -> Request:
    if row['allows_partial_payment'] not in {'true', 'false'}:
        raise ValueError('allows_partial_payment must be true or false')
    if row['request_type'] not in REQUEST_TYPES:
        raise ValueError(f'unknown request type: {row["request_type"]}')
    return Request(row['request_id'], row['user_id'], date.fromisoformat(row['request_date']),
                   row['request_type'], money(row['requested_amount']),
                   date.fromisoformat(row['desired_completion_date']),
                   row['allows_partial_payment'] == 'true', row['request_text'])


def parse_plan(value: str) -> tuple[Payment, ...]:
    if value in {'', 'none'}:
        return ()
    return tuple(Payment(date.fromisoformat(day), money(amount))
                 for day, amount in (part.split(':') for part in value.split('|')))


def parse_output(row: dict[str, str]) -> OutputRecord:
    changes = []
    if row['spending_changes_needed'] not in {'', 'none'}:
        for part in row['spending_changes_needed'].split('|'):
            pieces = part.split(':')
            if pieces[0] == 'stop' and len(pieces) == 2:
                changes.append(SpendingChange('stop', pieces[1]))
            elif pieces[0] == 'reduce_to' and len(pieces) == 3:
                changes.append(SpendingChange('reduce_to', pieces[1], money(pieces[2])))
            else:
                raise ValueError(f'invalid spending change: {part}')
    return OutputRecord(row['request_id'], optional_money(row['amount_safe_to_pay']),
                        row['affordability_status'] or None,
                        row['recommended_payment_method'] or None,
                        parse_plan(row['payment_plan']),
                        optional_date(row['earliest_date_for_full_payment']),
                        tuple(changes), row['decision_explanation'])


def unique(items: Iterable[T], key: str) -> dict[str, T]:
    result: dict[str, T] = {}
    for item in items:
        identity = getattr(item, key)
        if identity in result:
            raise ValueError(f'duplicate {key}: {identity}')
        result[identity] = item
    return result


@dataclass
class Dataset:
    profiles: dict[str, Profile]
    events: dict[str, Event]
    rates: dict[tuple[date, str, str], Decimal]
    requests: tuple[Request, ...]
    samples: tuple[Request, ...]
    options: tuple[PaymentOption, ...]
    messages: tuple[Message, ...]
    images: tuple[ImageEvidence, ...]
    output_template: tuple[OutputRecord, ...]

    def context(self, request: Request) -> RequestContext:
        events = tuple(e for e in self.events.values() if e.user_id == request.user_id)
        event_ids = {e.event_id for e in events}

        def relevant(user_id: str, request_id: str | None, event_id: str | None) -> bool:
            # Never leak another user's evidence. User-level evidence has no request ID.
            return user_id == request.user_id and (
                request_id == request.request_id or
                (request_id is None and (event_id is None or event_id in event_ids)))

        messages = tuple(sorted((m for m in self.messages if relevant(
            m.user_id, m.request_id, m.related_event_id) and
            m.sent_at.date() <= request.request_date), key=lambda m: (m.sent_at, m.message_id)))
        images = tuple(i for i in self.images if relevant(i.user_id, i.request_id, i.related_event_id))
        return RequestContext(request, self.profiles[request.user_id], events,
                              tuple(o for o in self.options if o.request_id == request.request_id),
                              messages, images, {key: value for key, value in self.rates.items()
                                                 if key[2] == self.profiles[request.user_id].home_currency})


def load_dataset(root: Path = REPO_ROOT) -> Dataset:
    base = root / 'dataset'

    def read(name: str, model: type) -> list[dict[str, str]]:
        return read_rows(base / f'{name}.csv', tuple(f.name for f in fields(model) if f.metadata.get('csv', True)))

    profiles = []
    for r in read('financial_profiles', Profile):
        if r['home_currency'] not in CURRENCIES or not tokens(r['payment_methods_user_will_consider']) <= METHODS:
            raise ValueError(f'invalid profile currency or methods: {r["user_id"]}')
        if r['max_installment_months'] and int(r['max_installment_months']) <= 0:
            raise ValueError('max_installment_months must be positive or blank')
        profiles.append(Profile(r['user_id'], r['home_currency'], money(r['current_available_balance']),
                                money(r['minimum_balance_to_keep']),
                                *(tokens(r[name]) for name in (
                                    'financial_priorities', 'expense_categories_to_protect',
                                    'expense_categories_user_is_willing_to_reduce',
                                    'expense_categories_user_is_willing_to_stop',
                                    'payment_methods_user_will_consider')),
                                int(r['max_installment_months']) if r['max_installment_months'] else None))
    events = []
    for r in read('financial_events', Event):
        if r['status'] not in {'settled', 'pending', 'scheduled', 'failed', 'cancelled', 'unrealized'}:
            raise ValueError(f'unknown event status: {r["status"]}')
        if r['direction'] not in {'debit', 'credit', 'non_cash'}:
            raise ValueError(f'unknown direction: {r["direction"]}')
        if r['event_type'] not in {'expense', 'debt_payment', 'subscription', 'income', 'refund',
                                   'investment_purchase', 'investment_valuation', 'investment_sale'}:
            raise ValueError(f'unknown event type: {r["event_type"]}')
        if r['flexibility'] not in {'fixed', 'stoppable', 'reducible', 'reducible_or_stoppable'}:
            raise ValueError(f'unknown flexibility: {r["flexibility"]}')
        if r['currency'] not in CURRENCIES:
            raise ValueError(f'unknown currency: {r["currency"]}')
        events.append(Event(r['event_id'], r['user_id'], r['event_type'], r['description'],
                            r['category'], r['direction'], optional_money(r['amount']), r['currency'],
                            date.fromisoformat(r['event_date']), optional_date(r['settlement_date']),
                            r['status'], r['linked_event_id'] or None, r['flexibility'],
                            optional_money(r['minimum_allowed_amount'])))
    rates = {}
    for r in read('exchange_rates', ExchangeRate):
        key = (date.fromisoformat(r['rate_date']), r['from_currency'], r['to_currency'])
        if key in rates or money(r['rate']) <= 0:
            raise ValueError(f'invalid or duplicate rate: {key}')
        rates[key] = money(r['rate'])
    options = tuple(PaymentOption(r['payment_option_id'], r['request_id'], r['payment_method'],
                                 money(r['payment_amount']), int(r['number_of_payments']),
                                 date.fromisoformat(r['first_payment_date']),
                                 int(r['payment_frequency_days']) if r['payment_frequency_days'] else None,
                                 money(r['financing_fee']), money(r['total_payable_amount']))
                    for r in read('request_payment_options', PaymentOption))
    messages = tuple(Message(r['message_id'], r['user_id'], r['request_id'] or None,
                             r['related_event_id'] or None, datetime.fromisoformat(r['sent_at']),
                             r['source_type'], r['message_text']) for r in read('messages', Message))
    images = tuple(ImageEvidence(r['image_id'], r['user_id'], r['request_id'] or None,
                                 r['related_event_id'] or None,
                                 base / 'media' / 'images' / f'{r["image_id"]}.png')
                   for r in read_rows(base / 'images.csv', ('image_id', 'user_id', 'request_id', 'related_event_id')))
    requests = tuple(parse_request(r) for r in read_rows(base / 'requests.csv', REQUEST_FIELDS))
    # Select only request inputs; solved fields are never stored in Dataset.
    samples = tuple(parse_request({key: r[key] for key in REQUEST_FIELDS}) for r in
                    read_rows(base / 'sample_requests.csv', REQUEST_FIELDS + OUTPUT_FIELDS[1:]))
    template = tuple(parse_output(r) for r in read_rows(base / 'output.csv', OUTPUT_FIELDS))
    data = Dataset(unique(profiles, 'user_id'), unique(events, 'event_id'), rates,
                   requests, samples, options, messages, images, template)
    all_requests = unique(requests + samples, 'request_id')
    unique(options, 'payment_option_id')
    unique(messages, 'message_id')
    unique(images, 'image_id')
    for option in options:
        if option.payment_method not in {'full_payment', 'installments'}:
            raise ValueError(f'unknown supplied payment method: {option.payment_method}')
    for message in messages:
        if message.sent_at.tzinfo is None:
            raise ValueError('message timestamp must include timezone')
        if message.source_type not in {'employer', 'service_provider', 'bank', 'merchant', 'financial_service'}:
            raise ValueError(f'unknown message source: {message.source_type}')
    for record in (*events, *requests, *samples, *messages, *images):
        if record.user_id not in data.profiles:
            raise ValueError(f'unknown user {record.user_id}')
    for record in (*options, *messages, *images):
        if record.request_id and record.request_id not in all_requests:
            raise ValueError(f'unknown request {record.request_id}')
    for e in events:
        if e.linked_event_id and (e.linked_event_id not in data.events or
                                 data.events[e.linked_event_id].user_id != e.user_id):
            raise ValueError(f'bad lifecycle link on {e.event_id}')
    for record in (*messages, *images):
        if record.request_id and all_requests[record.request_id].user_id != record.user_id:
            raise ValueError('evidence request and user disagree')
        if record.related_event_id and (record.related_event_id not in data.events or
                data.events[record.related_event_id].user_id != record.user_id):
            raise ValueError(f'bad evidence link: {record}')
    return data


def convert(amount: Decimal, source: str, target: str, day: date,
            rates: dict[tuple[date, str, str], Decimal]) -> Decimal:
    if source == target:
        return amount
    try:
        return amount * rates[(day, source, target)]
    except KeyError as exc:
        raise ValueError(f'missing dated FX {day} {source}->{target}') from exc
