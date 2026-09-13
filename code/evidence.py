"""Validate extracted facts, resolve conflicts, and return immutable event copies."""
from dataclasses import dataclass, field, replace
from datetime import date, datetime, time, timezone
from decimal import Decimal

from evidence_schemas import ImageFact, MessageFact
from evidence_rules import literal_amendment
from models import Event, Issue, RequestContext
from providers import EvidenceProvider, EvidenceUnavailable, source_for


@dataclass
class EvidenceResolution:
    events: tuple[Event, ...]
    issues: list[Issue] = field(default_factory=list)
    used: list[dict] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)


@dataclass(frozen=True)
class Claim:
    field: str
    value: object
    source_id: str
    source: str
    timestamp: datetime
    explicit: bool
    settled: bool


def preferred_claims(claims: list[Claim]) -> list[Claim]:
    """First three precedence steps; unresolved ties use conservative semantics."""
    top = max(c.explicit for c in claims)
    claims = [c for c in claims if c.explicit == top]
    latest: dict[str, datetime] = {}
    for c in claims:
        latest[c.source] = max(latest.get(c.source, c.timestamp), c.timestamp)
    claims = [c for c in claims if c.timestamp == latest[c.source]]
    if any(c.settled for c in claims):
        claims = [c for c in claims if c.settled]
    return claims


def choose_claim(claims: list[Claim], direction: str) -> Claim:
    """Explicit > latest within same source > settled > conservative value."""
    claims = preferred_claims(claims)

    def conservative(c: Claim):
        if isinstance(c.value, Decimal):
            return c.value if direction == 'debit' else -c.value
        if isinstance(c.value, date):
            return -c.value.toordinal() if direction == 'debit' else c.value.toordinal()
        if c.field in {'status', 'recurrence_cancelled'}:
            counts = c.value in {'settled', 'scheduled', 'pending', False}
            return int(counts) if direction == 'debit' else int(not counts)
        return str(c.value)
    return max(claims, key=lambda c: (conservative(c), c.source_id))


def proves_unresolved_debit(fact: MessageFact, context: RequestContext) -> bool:
    """Missing optional credit metadata cannot invalidate known cash capacity."""
    if fact.event_direction != 'debit' or fact.new_status in {'cancelled', 'failed', 'unrealized'}:
        return False
    if fact.new_status == 'pending':
        return True  # An authorization reserves cash even beyond the horizon.
    if fact.new_date is None:
        return True
    if fact.new_status == 'settled' and fact.new_date <= context.request.request_date:
        return False  # Already reflected in the opening snapshot.
    return fact.new_date <= context.request.horizon


def bind_next_payroll(fact: MessageFact, context: RequestContext) -> MessageFact:
    """Complete only a uniquely supported next payday; preserve literal amounts."""
    if not (fact.creates_new_event and fact.event_direction == 'credit' and fact.event_category == 'salary'
            and fact.new_amount is not None and fact.new_currency is not None
            and fact.new_date is None and fact.new_status == 'scheduled'
            and ('next salary' in (fact.event_description or '').casefold()
                 or 'next payroll' in (fact.evidence_summary or '').casefold())):
        return fact
    from reconstruction import REGULAR_PAY, UNCERTAIN_PAY, add_months, recurring_kind
    groups: dict[str, list[Event]] = {}
    for e in context.events:
        if (e.status == 'settled' and e.direction == 'credit' and e.category == 'salary'
                and e.currency == fact.new_currency and e.settlement_date and e.settlement_date <= context.request.request_date
                and REGULAR_PAY.search(e.description) and not UNCERTAIN_PAY.search(e.description)):
            groups.setdefault(e.description.casefold(), []).append(e)
    candidates = []
    for history in groups.values():
        history.sort(key=lambda e: e.settlement_date)
        kind = recurring_kind(history, salary=True)
        if kind and kind[0] == 'monthly':
            day = add_months(history[-1].settlement_date, 1, kind[1])
            if context.request.request_date <= day <= context.request.horizon:
                candidates.append((history[-1], day))
    if len(candidates) != 1:
        return fact
    target, day = candidates[0]
    return fact.model_copy(update={'creates_new_event': False, 'related_event_id': target.event_id,
                                  'new_date': day, 'action': 'amend'})


def resolve_evidence(context: RequestContext, provider: EvidenceProvider) -> EvidenceResolution:
    result = EvidenceResolution(tuple(replace(e) for e in context.events))
    originals = {e.event_id: e for e in context.events}
    claims: dict[str, dict[str, list[Claim]]] = {}
    created: list[Event] = []
    proposed_sources: dict[str, dict] = {}
    for record in (*context.images, *context.messages):
        identity = getattr(record, 'image_id', None) or getattr(record, 'message_id', '')
        try:
            source = source_for(record)
            facts = provider.resolve(source, context)
        except (EvidenceUnavailable, OSError) as exc:
            code = 'missing_image_file' if isinstance(exc, OSError) else 'unresolved_evidence'
            facts = literal_amendment(record, context)
            if facts is None:
                result.issues.append(Issue(code, identity, 'source unavailable or not cached; no value imputed'))
                result.skipped.append({'source_id': identity, 'reason': code})
                continue
            result.used.append({'source_id': identity, 'action': 'literal_percentage_fallback',
                                'reason': 'uncached; exact financial sentence and unique monthly lease'})
        extracted = [*facts.images, *facts.messages]
        if not extracted:
            result.skipped.append({'source_id': identity, 'reason': 'no financial facts'})
        for index, fact in enumerate(extracted):
            reason = None
            if fact.source_id != identity:
                reason = 'source identity mismatch'
            elif isinstance(fact, ImageFact) != (source.kind == 'image'):
                reason = 'fact/source modality mismatch'
            elif fact.confidence < 0.8:
                reason = 'low confidence; requires review'
            elif record.related_event_id and fact.related_event_id != record.related_event_id:
                reason = 'fact contradicts supplied event link'
            elif fact.related_event_id and fact.related_event_id not in originals:
                reason = 'event is not in this user context'
            elif isinstance(fact, MessageFact) and fact.action == 'irrelevant':
                reason = 'irrelevant'
            if reason:
                result.skipped.append({'source_id': identity, 'reason': reason})
                if reason != 'irrelevant':
                    result.issues.append(Issue('rejected_fact', identity, reason))
                continue
            if isinstance(fact, MessageFact):
                fact = bind_next_payroll(fact, context)
            target = originals.get(fact.related_event_id or '')
            if isinstance(fact, MessageFact) and fact.creates_new_event:
                if target is not None:
                    result.issues.append(Issue('rejected_fact', identity, 'new event duplicates an existing linked fact'))
                    continue
                required = (fact.event_description, fact.event_category, fact.event_direction,
                            fact.event_type, fact.new_currency, fact.new_date, fact.new_status)
                if not all(required):
                    result.issues.append(Issue('incomplete_new_fact', identity,
                                               'new event requires explicit description/category/direction/type/currency/date/status',
                                               proves_unresolved_debit(fact, context)))
                    continue
                if fact.new_currency not in {'INR', 'EUR', 'USD', 'IDR', 'ZAR'} or fact.event_type not in {
                        'income', 'expense', 'subscription', 'debt_payment', 'refund', 'investment_purchase', 'investment_sale'}:
                    result.issues.append(Issue('rejected_fact', identity, 'unsupported new event currency/type',
                                               proves_unresolved_debit(fact, context)))
                    continue
                created.append(Event(f'evidence_{identity}_{index}', context.request.user_id,
                    fact.event_type, fact.event_description, fact.event_category, fact.event_direction,
                    Decimal(fact.new_amount) if fact.new_amount is not None else None, fact.new_currency,
                    context.request.request_date, fact.new_date, fact.new_status, None, 'fixed', None,
                    evidence_ids=(identity,), recurrence_reason='Explicit new fact; no recurrence inferred from one observation'))
                result.used.append({'source_id': identity, 'event_id': created[-1].event_id, 'action': 'create_fact'})
                continue
            if target is None:
                result.issues.append(Issue('unlinked_fact', identity, 'no unambiguous existing event or complete new fact'))
                result.skipped.append({'source_id': identity, 'reason': 'unlinked fact'})
                continue
            updates: dict[str, object] = {}
            if isinstance(fact, ImageFact):
                if fact.amount is not None:
                    updates['amount'] = Decimal(fact.amount)
                if fact.currency is not None:
                    updates['currency'] = fact.currency
                if fact.status is not None:
                    updates['status'] = fact.status
                if fact.effective_date is not None:
                    updates['settlement_date'] = fact.effective_date
                if fact.direction is not None and fact.direction != target.direction:
                    result.issues.append(Issue('direction_conflict', identity, 'image contradicts event cash direction', True))
                    continue
                timestamp = datetime.combine(fact.effective_date or target.event_date, time.min, timezone.utc)
                source_group = f'image:{fact.document_type}'
                explicit = False
                settled = fact.status == 'settled'
            else:
                timestamp = record.sent_at
                source_group = record.source_type
                explicit = fact.action in {'cancel', 'settle', 'amend', 'delay'}
                settled = fact.action == 'settle' or fact.new_status == 'settled'
                new_amount = Decimal(fact.new_amount) if fact.new_amount is not None else None
                if fact.percentage_change is not None:
                    if new_amount is not None or target.amount is None:
                        result.issues.append(Issue('ambiguous_percentage', identity, 'percentage needs one known base amount and no conflicting absolute amount'))
                        continue
                    new_amount = target.amount * (Decimal('1') + Decimal(fact.percentage_change) / Decimal('100'))
                if fact.action in {'amend', 'delay', 'confirm'} and all(v is None for v in
                        (new_amount, fact.new_currency, fact.new_date, fact.new_status)):
                    result.issues.append(Issue('incomplete_amendment', identity, 'no concrete amount, percentage, date, currency or status to apply'))
                    result.skipped.append({'source_id': identity, 'reason': 'incomplete amendment'})
                    continue
                if fact.scope == 'future_recurrence':
                    if fact.action == 'cancel':
                        updates['recurrence_cancelled'] = True
                    if new_amount is not None:
                        updates['recurrence_override_amount'] = new_amount
                    updates['recurrence_override_date'] = fact.new_date or context.request.request_date
                    if fact.action == 'delay' and fact.new_date is not None:
                        updates['recurrence_override_day'] = fact.new_date.day
                    updates['recurrence_reason'] = f'Explicit recurring amendment {identity}'
                else:
                    if new_amount is not None:
                        updates['amount'] = new_amount
                    if fact.new_date is not None:
                        updates['settlement_date'] = fact.new_date
                    if fact.new_status is not None:
                        updates['status'] = fact.new_status
                    if fact.action == 'cancel':
                        updates['status'] = 'cancelled'
                    elif fact.action == 'settle':
                        updates['status'] = 'settled'
                    elif fact.new_date and fact.new_date > context.request.request_date:
                        updates.setdefault('status', 'scheduled')
                if fact.new_currency is not None:
                    updates['recurrence_override_currency' if fact.scope == 'future_recurrence' else 'currency'] = fact.new_currency
            if updates.get('currency', target.currency) not in {'INR', 'EUR', 'USD', 'IDR', 'ZAR'} or updates.get('recurrence_override_currency', target.currency) not in {'INR', 'EUR', 'USD', 'IDR', 'ZAR'}:
                result.issues.append(Issue('unknown_currency', identity, 'unsupported extracted currency', True))
                continue
            if not updates:
                result.skipped.append({'source_id': identity, 'reason': 'no concrete amended values'})
                continue
            proposed_sources[identity] = {'source_id': identity, 'event_id': target.event_id,
                                          'action': fact.action if isinstance(fact, MessageFact) else 'image_fact'}
            for name, value in updates.items():
                slots = claims.setdefault(target.event_id, {}).setdefault(name, [])
                slots.append(Claim(name, value, identity, source_group, timestamp, explicit, settled))
    resolved = []
    used_ids: set[str] = set()
    for event in context.events:
        updates = {}
        ids = set(event.evidence_ids)
        prospective = bool(event.settlement_date and event.settlement_date <= context.request.request_date and any(
            isinstance(c.value, date) and c.value > context.request.request_date
            for c in claims.get(event.event_id, {}).get('settlement_date', [])))
        for name, options in claims.get(event.event_id, {}).items():
            current = getattr(event, name)
            if not prospective and current is not None and name not in {'recurrence_reason', 'recurrence_cancelled'}:
                options = options + [Claim(name, current, event.event_id, 'structured',
                    datetime.combine(event.event_date, time.min, timezone.utc),
                    name == 'status' and current == 'cancelled', event.status == 'settled')]
            # A missing event amount can be filled by document evidence. Settled original
            # facts otherwise retain their specified priority against estimates.
            chosen = choose_claim(options, event.direction)
            if name in {'currency', 'recurrence_override_currency'} and len({c.value for c in preferred_claims(options)}) > 1:
                result.issues.append(Issue('currency_conflict', event.event_id,
                                           'conflicting extracted currencies require reconciliation before cash certification', True))
            updates[name] = chosen.value
            if chosen.source_id != event.event_id:
                ids.add(chosen.source_id)
                used_ids.add(chosen.source_id)
        if updates and event.settlement_date and event.settlement_date <= context.request.request_date and (
                updates.get('settlement_date', event.settlement_date) > context.request.request_date):
            # A next-payment confirmation must not erase the historical observation.
            resolved.append(replace(event))
            resolved.append(replace(event, **updates, event_id=f'{event.event_id}_next',
                                    linked_event_id=None, evidence_ids=tuple(sorted(ids))))
        else:
            resolved.append(replace(event, **updates, evidence_ids=tuple(sorted(ids))))
    for identity, proposal in proposed_sources.items():
        if identity in used_ids:
            result.used.append(proposal)
        else:
            result.skipped.append({**proposal, 'reason': 'superseded by conflict precedence'})
    result.events = tuple(resolved + created)
    return result


def unresolved_evidence(context: RequestContext) -> list[Issue]:
    issues = [Issue('unresolved_message', m.message_id,
                    f'{m.source_type}; event={m.related_event_id or "user/request level"}; '
                    'text requires interpretation; structured-only forecast is provisional')
              for m in context.messages]
    for image in context.images:
        issues.append(Issue('unresolved_image' if image.path.is_file() else 'missing_image_file',
                            image.image_id, f'event={image.related_event_id}; {image.path}'))
    return issues
