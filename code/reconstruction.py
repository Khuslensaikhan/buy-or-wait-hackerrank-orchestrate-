"""Resolve cash states and infer conservative recurring streams from input evidence."""
import calendar
import re
from collections import defaultdict
from dataclasses import replace
from datetime import date, timedelta
from decimal import Decimal, ROUND_CEILING

from data_loader import convert
from evidence import unresolved_evidence
from models import CashFlow, Event, Issue, Reconstruction, RequestContext

VARIABLE_CATEGORIES = frozenset({'groceries', 'transport', 'dining'})
UNCERTAIN_PAY = re.compile(r'bonus|commission|arrears|freelance|contract|platform|'
                           r'earnings|payout|seasonal|temporary|prorated|milestone', re.I)
REGULAR_PAY = re.compile(r'payroll|base salary|household salary|employer salary', re.I)
FINAL_PAY = re.compile(r'final.*(?:payroll|salary)|(?:payroll|salary).*final', re.I)
ONE_TIME = re.compile(r'\bone[ -](?:off|time)\b|\boutstanding\b|\bdelivered\b|'
                      r'\bauthori[sz]ation\b|\brevers(?:ed|al)\b|\brefund\b|\bretry\b', re.I)
CONTRACTUAL_CATEGORIES = frozenset({'rent', 'housing', 'insurance', 'education', 'debt_repayment'})


def expense_kind(event: Event) -> str:
    """A dated receipt or arrears balance is not the ongoing household budget."""
    if ONE_TIME.search(event.description):
        return 'one_time'
    if event.event_type in {'subscription', 'debt_payment'} or event.category in CONTRACTUAL_CATEGORIES:
        return 'contractual'
    return 'variable'


def estimate_debit(history: list[Event]) -> Decimal:
    known = [e.amount for e in history if e.amount is not None]
    if expense_kind(history[-1]) == 'contractual':
        return known[-1]
    # Estimate the repeated budget from all observations, rather than repeating
    # one recent high purchase for 90 days. Round debits up, capacity down.
    return (sum(known) / len(known)).quantize(Decimal('.01'), rounding=ROUND_CEILING)


def stream_identity(event: Event) -> tuple[str, ...]:
    """Every observation belongs to exactly one stream, including at merchants."""
    pooled = event.direction == 'debit' and event.event_type == 'expense' and event.category in VARIABLE_CATEGORIES
    identity = event.category if pooled else event.description.casefold()
    return event.direction, event.event_type, event.category, event.currency, identity


def add_months(day: date, months: int, anchor_day: int | None = None) -> date:
    index = day.year * 12 + day.month - 1 + months
    year, month0 = divmod(index, 12)
    month = month0 + 1
    return date(year, month, min(anchor_day or day.day, calendar.monthrange(year, month)[1]))


def resolve_lifecycle(events: tuple[Event, ...]) -> tuple[Event, ...]:
    """Suppress replacements, not distinct refund/sale cash legs or disputed debits."""
    by_id = {e.event_id: e for e in events}
    suppressed: set[str] = set()
    for event in events:
        parent = by_id.get(event.linked_event_id or '')
        seen = {event.event_id}
        same_cash_leg = True
        while parent:
            if parent.event_id in seen:
                raise ValueError(f'cyclic lifecycle link: {event.event_id}')
            seen.add(parent.event_id)
            same_cash_leg = same_cash_leg and parent.direction == event.direction
            if same_cash_leg and event.status in {'settled', 'cancelled'}:
                if parent.status in {'pending', 'scheduled', 'failed', 'cancelled'}:
                    suppressed.add(parent.event_id)
            parent = by_id.get(parent.linked_event_id or '')
    return tuple(e for e in events if e.event_id not in suppressed and
                 e.status not in {'failed', 'cancelled', 'unrealized'} and
                 e.direction != 'non_cash')


def recurring_kind(events: list[Event], *, salary: bool = False) -> tuple[str, int] | None:
    days = sorted({e.settlement_date for e in events if e.settlement_date})
    if len(days) < 3:
        return None
    # Monthly first: avoid inferring a 28/30-day drift for calendar bills.
    indices = [d.year * 12 + d.month for d in days]
    anchor = max(d.day for d in days)
    if all(b - a == 1 for a, b in zip(indices, indices[1:])) and all(
            d.day == min(anchor, calendar.monthrange(d.year, d.month)[1]) for d in days):
        return 'monthly', anchor
    if salary and all(b - a == 1 for a, b in zip(indices, indices[1:])):
        # Payroll settlement can shift with weekends or an employer delay. One
        # observation per consecutive month supports monthly pay, not an exact
        # elapsed-day interval. Retain the later recent payday conservatively.
        return 'monthly', max(d.day for d in days[-3:])
    gaps = [(b - a).days for a, b in zip(days, days[1:])]
    if len(set(gaps)) == 1 and 1 <= gaps[0] <= 31:
        return 'interval', gaps[0]
    return None


def reconstruct(context: RequestContext,
                rates: dict[tuple[date, str, str], Decimal],
                evidence_issues: list[Issue] | None = None) -> Reconstruction:
    request, profile = context.request, context.profile
    start, end = request.request_date, request.horizon
    result = Reconstruction(issues=unresolved_evidence(context) if evidence_issues is None else list(evidence_issues),
                            resolved_events=context.events)
    active = resolve_lifecycle(context.events)

    def emit(event: Event, day: date, amount: Decimal | None,
             inferred: bool = False, fx_day: date | None = None, reason: str = "") -> None:
        if not start <= day <= end:
            return
        if amount is None:
            result.issues.append(Issue('missing_active_amount', event.event_id,
                                       f'{event.direction} on {day}; amount requires image interpretation',
                                       blocking=event.direction == 'debit'))
            return
        try:
            home = convert(amount, event.currency, profile.home_currency, fx_day or day, rates)
        except ValueError as exc:
            result.issues.append(Issue('missing_fx', event.event_id, str(exc),
                                       blocking=event.direction == 'debit'))
            return
        result.flows.append(CashFlow(day, -home if event.direction == 'debit' else home,
                                     event.event_id, inferred,
                                     direction=event.direction, classification='projected' if inferred else 'original',
                                     essential=event.category in {'rent', 'housing', 'utilities', 'groceries', 'transport',
                                                                 'healthcare', 'insurance', 'education', 'debt_repayment', 'family_support'},
                                     protected=event.category in profile.expense_categories_to_protect,
                                     flexibility=event.flexibility,
                                     recurrence_reason=reason or 'Explicit cash event; no recurrence expansion',
                                     evidence_ids=event.evidence_ids, original_amount=amount,
                                     original_currency=event.currency,
                                     conversion_rate=convert(Decimal('1'), event.currency, profile.home_currency, fx_day or day, rates)))

    for event in active:
        day = event.settlement_date
        if day is None:
            result.issues.append(Issue('missing_settlement_date', event.event_id,
                                       'cash event lacks settlement date', event.direction == 'debit'))
            continue
        if event.status == 'pending':
            if event.direction == 'debit':
                emit(event, start, event.amount, fx_day=day)
            continue
        if day <= start and event.status == 'settled':
            if event.amount is None:
                result.issues.append(Issue('missing_historical_amount', event.event_id,
                                           'already in cash snapshot; recurrence/evidence unresolved'))
            continue
        if event.status == 'scheduled' and event.direction == 'credit' and not (
                event.category == 'salary' and not UNCERTAIN_PAY.search(event.description)):
            result.issues.append(Issue('unconfirmed_credit', event.event_id,
                                       'non-salary credit omitted until settlement'))
            continue
        emit(event, max(start, day), event.amount)

    groups: dict[tuple[str, ...], list[Event]] = defaultdict(list)
    image_transactions = {i.related_event_id for i in context.images}
    descriptions: dict[tuple[str, ...], int] = defaultdict(int)
    for event in active:
        descriptions[(event.direction, event.category, event.currency, event.description.casefold())] += 1
    for event in active:
        if event.status != 'settled' or not event.settlement_date or event.settlement_date > start:
            continue
        if event.direction == 'credit':
            if event.category != 'salary' or UNCERTAIN_PAY.search(event.description) or not REGULAR_PAY.search(event.description):
                continue
        elif event.event_type not in {'expense', 'subscription', 'debt_payment'}:
            continue
        elif expense_kind(event) == 'one_time':
            continue
        elif (event.event_id in image_transactions and event.category in VARIABLE_CATEGORIES
              and descriptions[(event.direction, event.category, event.currency, event.description.casefold())] == 1):
            # A separately supplied receipt with no repeated merchant history is
            # an individual purchase, not another observation of the usual budget.
            # Its cash state was already handled above, including pending reserves.
            continue
        groups[stream_identity(event)].append(event)

    # A prorated first paycheck plus an explicit next regular salary establishes
    # the monthly employment stream. Neither a lone salary nor an uncertain bonus
    # is sufficient. The prorated amount is not the ongoing salary estimate.
    if not any(k[0] == 'credit' for k in groups):
        starters = [e for e in active if e.status == 'settled' and e.category == 'salary'
                    and e.direction == 'credit' and 'prorated first salary' in e.description.casefold()]
        for first in starters:
            confirmations = [e for e in active if e.status == 'scheduled' and e.category == 'salary'
                             and e.direction == 'credit' and e.currency == first.currency
                             and 'confirmed salary' in e.description.casefold() and e.amount is not None
                             and first.settlement_date and e.settlement_date == add_months(first.settlement_date, 1)]
            if len(confirmations) == 1:
                regular = confirmations[0]
                key = ('credit', 'income', 'salary', regular.currency, regular.description.casefold())
                groups[key].append(replace(first, description=regular.description, amount=regular.amount))

    for key, history in sorted(groups.items()):
        history.sort(key=lambda e: (e.settlement_date, e.event_id))
        last = history[-1]
        salary = last.direction == 'credit'
        salary_streams = sum(k[0] == 'credit' and k[3] == last.currency for k in groups)
        future_salary = [e for e in active if salary and e.direction == 'credit' and e.category == 'salary'
                         and e.currency == last.currency and e.status == 'scheduled'
                         and e.settlement_date and e.settlement_date > start
                         and not UNCERTAIN_PAY.search(e.description)
                         and (e.description.casefold() == last.description.casefold() or salary_streams == 1)]
        observations = history + future_salary
        kind = recurring_kind(observations, salary=salary) if salary else recurring_kind(history)
        if salary and len(history) == 1 and len(future_salary) == 1 and any(
                e.event_id == last.event_id and 'prorated first salary' in e.description.casefold() for e in active):
            kind = ('monthly', future_salary[0].settlement_date.day)
        if kind is None:
            if len(history) >= 3:
                result.issues.append(Issue('irregular_history', history[-1].event_id,
                                           f'no supported cadence for {key[-1]}'))
            continue
        mode, cadence = kind
        assert last.settlement_date is not None
        last_day = last.settlement_date
        next_day = add_months(last_day, 1, cadence) if mode == 'monthly' else last_day + timedelta(days=cadence)
        if next_day < start:
            result.issues.append(Issue('stale_recurrence', last.event_id,
                                       f'{key[-1]}: expected next occurrence {next_day} already overdue'))
            continue
        if last.direction == 'credit' and any(FINAL_PAY.search(e.description) and
                e.settlement_date and e.settlement_date >= last_day for e in active):
            result.issues.append(Issue('ended_income', last.event_id, 'final payroll prevents extrapolation'))
            continue
        known = [e.amount for e in history if e.amount is not None]
        if not known:
            result.issues.append(Issue('unknown_recurring_amount', last.event_id,
                                       f'no known amounts for {key[-1]}', last.direction == 'debit'))
            continue
        amount = known[-1] if last.direction == 'credit' else estimate_debit(history)
        if salary and len(future_salary) == 1:
            confirmed_amount = future_salary[0].amount
            # A confirmed return to an established rate brackets a temporary dip;
            # a new, higher one-off figure does not authorize a permanent raise.
            if confirmed_amount is not None and known.count(confirmed_amount) >= 3:
                amount = confirmed_amount
        estimator = 'supported salary rate' if salary else (
            'latest contractual amount' if expense_kind(last) == 'contractual' else 'mean historical budget, rounded up')
        reason = f'{key[-1]}; {mode}={cadence}; observations={len(history)}; {estimator}={amount}'
        result.recurrence.append(f'{last.event_id}: {reason}')
        overrides = sorted((e for e in history if e.recurrence_override_date is not None),
                           key=lambda e: (e.recurrence_override_date, e.event_id))
        step = 1
        while next_day <= end:
            # Explicit matching future records substitute for inferred occurrences.
            # Salary descriptions may change for a confirmed next payroll.
            explicit = [e for e in context.events if e.settlement_date and e.settlement_date >= start and
                        e.direction == last.direction and e.category == last.category and
                        e.currency == last.currency and
                        (stream_identity(e) == key or
                         (salary and salary_streams == 1 and not UNCERTAIN_PAY.search(e.description))) and
                        (e.settlement_date == next_day or (mode == 'monthly' and
                         (e.settlement_date.year, e.settlement_date.month) == (next_day.year, next_day.month)))]
            projected = last
            projected_amount = amount
            cancelled = False
            payment_day = next_day
            for amendment in overrides:
                if mode == 'monthly' and amendment.recurrence_override_day and (
                        amendment.recurrence_override_date.year, amendment.recurrence_override_date.month) <= (next_day.year, next_day.month):
                    payment_day = next_day.replace(day=min(amendment.recurrence_override_day,
                                                          calendar.monthrange(next_day.year, next_day.month)[1]))
                if amendment.recurrence_override_date <= payment_day:
                    cancelled = amendment.recurrence_cancelled
                    if amendment.recurrence_override_amount is not None:
                        projected_amount = amendment.recurrence_override_amount
                    if amendment.recurrence_override_currency is not None:
                        projected = replace(projected, currency=amendment.recurrence_override_currency)
                    projected = replace(projected, evidence_ids=tuple(sorted(set(projected.evidence_ids + amendment.evidence_ids))))
            if not explicit and not cancelled:
                emit(projected, payment_day, projected_amount, inferred=True,
                     reason=reason + ('; applied evidence ' + ','.join(projected.evidence_ids) if projected.evidence_ids else ''))
            step += 1
            next_day = add_months(last_day, step, cadence) if mode == 'monthly' else last_day + timedelta(days=cadence * step)
    result.flows.sort(key=lambda f: (f.day, f.amount >= 0, f.source_id))
    return result
