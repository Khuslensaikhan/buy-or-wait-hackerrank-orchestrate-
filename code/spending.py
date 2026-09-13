"""Bounded-cardinality spending-change search, with optimistic pruning and re-simulation."""
from dataclasses import replace
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from itertools import combinations, product

from forecast import simulate
from models import CENT, ZERO, Candidate, CashFlow, Reconstruction, RequestContext, SpendingChange


def validate_changes(changes: tuple[SpendingChange, ...], context: RequestContext,
                     state: Reconstruction) -> list[str]:
    errors = []
    if len(changes) > 3:
        errors.append('maximum three spending changes')
    if len({c.event_id for c in changes}) != len(changes):
        errors.append('duplicate event change; stop and reduce are mutually exclusive')
    events = {e.event_id: e for e in context.events}
    profile = context.profile
    for change in changes:
        event = events.get(change.event_id)
        flows = [f for f in state.flows if f.source_id == change.event_id and f.inferred and f.amount < 0]
        if event is None or not flows:
            errors.append(f'{change.event_id}: not a supported recurring expense')
            continue
        if event.category in profile.expense_categories_to_protect or event.flexibility == 'fixed' or any(f.protected for f in flows):
            errors.append(f'{change.event_id}: protected or fixed expense')
        if change.action == 'stop':
            if change.amount is not None:
                errors.append('stop must not have an amount')
            if event.flexibility not in {'stoppable', 'reducible_or_stoppable'} or event.category not in profile.expense_categories_user_is_willing_to_stop:
                errors.append(f'{change.event_id}: stopping not permitted')
        elif change.action == 'reduce_to':
            if event.flexibility not in {'reducible', 'reducible_or_stoppable'} or event.category not in profile.expense_categories_user_is_willing_to_reduce:
                errors.append(f'{change.event_id}: reduction not permitted')
            if change.amount is None or not change.amount.is_finite() or event.minimum_allowed_amount is None or event.amount is None:
                errors.append(f'{change.event_id}: missing reduction amount or floor')
            elif not event.minimum_allowed_amount <= change.amount < event.amount:
                errors.append(f'{change.event_id}: reduction violates floor or does not reduce spending')
            elif any(f.original_amount is None or change.amount >= f.original_amount for f in flows):
                errors.append(f'{change.event_id}: reduction must lower each affected projected amount')
        else:
            errors.append('unknown spending action')
    return errors


def apply_changes(flows: list[CashFlow], changes: tuple[SpendingChange, ...]) -> list[CashFlow]:
    by_id = {c.event_id: c for c in changes}
    result = []
    for flow in flows:
        change = by_id.get(flow.source_id) if flow.inferred and flow.amount < 0 else None
        if change is None:
            result.append(flow)
        elif change.action == 'stop':
            result.append(replace(flow, amount=ZERO))
        else:
            assert change.amount is not None
            result.append(replace(flow, amount=-change.amount * flow.conversion_rate))
    return result


def change_options(context: RequestContext, state: Reconstruction) -> list[tuple[SpendingChange, ...]]:
    result = []
    for event in sorted(context.events, key=lambda e: e.event_id):
        possibilities = [SpendingChange('stop', event.event_id)]
        if event.minimum_allowed_amount is not None:
            possibilities.append(SpendingChange('reduce_to', event.event_id, event.minimum_allowed_amount))
        valid = tuple(c for c in possibilities if not validate_changes((c,), context, state))
        if valid:
            result.append(valid)
    return result


def search_changes(candidate: Candidate, context: RequestContext, state: Reconstruction) -> list[Candidate]:
    if state.blocked or not candidate.payments or any(p.day < context.request.request_date or
            p.day > min(context.request.desired_completion_date, context.request.horizon) for p in candidate.payments):
        return []
    baseline = simulate(context.request, context.profile, state.flows, candidate.payments)
    if baseline.safe:
        return []
    options = change_options(context, state)
    deficit = context.profile.minimum_balance_to_keep - baseline.minimum_balance
    savings = {c: sum((b.amount - a.amount for a, b in zip(state.flows, apply_changes(state.flows, (c,)))), ZERO)
               for group in options for c in group}
    results = []
    for count in range(1, min(3, len(options)) + 1):
        for groups in combinations(options, count):
            # Optimistic upper bound: even all savings over the horizon are insufficient.
            if sum((max(savings[c] for c in g) for g in groups), ZERO) < deficit:
                continue
            for combo in product(*groups):
                if sum((savings[c] for c in combo), ZERO) < deficit:
                    continue
                if not simulate(context.request, context.profile, apply_changes(state.flows, combo), candidate.payments).safe:
                    continue
                tightened = list(combo)
                for i, change in enumerate(tightened):
                    if change.action != 'reduce_to':
                        continue
                    event = next(e for e in context.events if e.event_id == change.event_id)
                    lo = int((change.amount / CENT).to_integral_value(rounding=ROUND_CEILING))
                    hi = int((event.amount / CENT).to_integral_value(rounding=ROUND_FLOOR)) - 1
                    while lo < hi:
                        mid = (lo + hi + 1) // 2
                        attempt = tuple(tightened[:i] + [replace(change, amount=mid * CENT)] + tightened[i+1:])
                        if simulate(context.request, context.profile, apply_changes(state.flows, attempt), candidate.payments).safe:
                            lo = mid
                        else:
                            hi = mid - 1
                    tightened[i] = replace(change, amount=lo * CENT)
                changes = tuple(tightened)
                if validate_changes(changes, context, state) or not simulate(context.request, context.profile,
                        apply_changes(state.flows, changes), candidate.payments).safe:
                    continue
                reasons = []
                for i, change in enumerate(changes):
                    without = changes[:i] + changes[i+1:]
                    check = simulate(context.request, context.profile, apply_changes(state.flows, without), candidate.payments)
                    reasons.append(f'{change.action}:{change.event_id}: without this change, '
                                   f'minimum {check.minimum_balance} breaches reserve on {check.breach_date}')
                results.append(replace(candidate, changes=changes, change_reasons=tuple(reasons)))
        if results:
            break  # Smallest sufficient change count for this payment schedule.
    return results
