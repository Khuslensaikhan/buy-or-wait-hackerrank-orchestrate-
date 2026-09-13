"""Generate, validate and rank plans without access to solved outputs."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from forecast import earliest_full_payment, safe_capacity, simulate
from models import (ZERO, Candidate, Decision, Payment, PredictionResult,
                    Reconstruction, RequestContext)
from reconstruction import add_months
from spending import apply_changes, search_changes, validate_changes


def rank(candidate: Candidate) -> tuple[bool, int, Decimal, date, int, str]:
    # Deadline violations are rejected before ranking. Change count is not a ranking criterion.
    return (False, int(bool(candidate.changes)), candidate.total_cost, candidate.payments[0].day,
            len(candidate.payments), candidate.option_id)


def validate_candidate(candidate: Candidate, context: RequestContext,
                       reconstruction: Reconstruction, safe: Decimal,
                       earliest: date | None) -> list[str]:
    request, profile = context.request, context.profile
    reasons = validate_changes(candidate.changes, context, reconstruction)
    payments = candidate.payments
    if reconstruction.blocked:
        reasons.append('unresolved active debit prevents safety certification')
    if not payments:
        return reasons + ['empty payment plan']
    if tuple(sorted(payments, key=lambda p: p.day)) != payments:
        reasons.append('payments not chronological')
    if any(p.amount <= 0 for p in payments):
        reasons.append('payments must be positive')
    if any(p.day < request.request_date or p.day > min(request.horizon, request.desired_completion_date)
           for p in payments):
        reasons.append('payment outside request/deadline/forecast bounds')
    method = 'full_payment' if candidate.method == 'wait' else candidate.method
    if method not in profile.payment_methods_user_will_consider:
        reasons.append('payment method excluded by user')
    if candidate.method == 'partial_payment':
        expected = (Payment(request.request_date, safe),
                    Payment(earliest, request.requested_amount - safe)) if earliest else ()
        if not request.allows_partial_payment or not ZERO < safe < request.requested_amount:
            reasons.append('partial payment not permitted or no strictly partial capacity')
        if payments != expected or len(payments) != 2 or sum((p.amount for p in payments), ZERO) != request.requested_amount:
            reasons.append('partial plan must pay safe amount now and exact remainder on earliest date')
    elif candidate.method in {'full_payment', 'wait'}:
        expected_day = request.request_date if candidate.method == 'full_payment' else (payments[0].day if candidate.changes else earliest)
        if payments != (Payment(expected_day, request.requested_amount),):
            reasons.append('full/wait payment does not match amount and capacity date')
        if candidate.method == 'wait' and (payments[0].day <= request.request_date or (not candidate.changes and earliest is None)):
            reasons.append('wait requires a later safe full-payment date')
    elif candidate.method == 'installments':
        option = next((o for o in context.options if o.payment_option_id == candidate.option_id), None)
        if option is None or option.payment_method != 'installments':
            reasons.append('no supplied installment option')
        else:
            if payments != option.payments() or candidate.total_cost != option.total_payable_amount:
                reasons.append('installments differ from supplied option')
            limit = profile.max_installment_months
            if limit is None or option.number_of_payments > limit or (limit is not None and
                    payments[-1].day > add_months(payments[0].day, limit)):
                reasons.append('installment duration/count exceeds user limit')
            if option.number_of_payments < 2:
                reasons.append('installments require at least two payments')
            if option.total_payable_amount != request.requested_amount + option.financing_fee:
                reasons.append('stated total does not equal principal plus fee')
            if sum((p.amount for p in payments), ZERO) != option.total_payable_amount:
                reasons.append('installment sum must equal stated total exactly')
    else:
        reasons.append('unknown method')
    if candidate.method != 'installments' and candidate.total_cost != request.requested_amount:
        reasons.append('non-installment total must equal principal')
    if not any('bounds' in r or 'positive' in r for r in reasons):
        simulation = simulate(request, profile, apply_changes(reconstruction.flows, candidate.changes), payments)
        if not simulation.safe:
            reasons.append(f'minimum balance breached on {simulation.breach_date}: {simulation.minimum_balance}')
    return reasons



@dataclass(frozen=True)
class CandidateVerification:
    candidate: Candidate
    checks: dict[str, bool]
    errors: tuple[str, ...]
    minimum_balance: Decimal | None

    @property
    def valid(self) -> bool:
        return not self.errors and all(self.checks.values())


def generate_candidate_plans(context: RequestContext, state: Reconstruction, safe: Decimal,
                             earliest: date | None) -> list[Candidate]:
    request = context.request
    full_id = min((o.payment_option_id for o in context.options if o.payment_method == 'full_payment'), default='')
    candidates = [Candidate('full_payment', (Payment(request.request_date, request.requested_amount),),
                            request.requested_amount, full_id)]
    if earliest and earliest > request.request_date:
        candidates.append(Candidate('wait', (Payment(earliest, request.requested_amount),), request.requested_amount, full_id))
        if ZERO < safe < request.requested_amount:
            candidates.append(Candidate('partial_payment', (
                Payment(request.request_date, safe), Payment(earliest, request.requested_amount - safe)), request.requested_amount))
    for option in context.options:
        if option.payment_method == 'installments':
            candidates.append(Candidate('installments', option.payments(), option.total_payable_amount, option.payment_option_id))
    changed_bases = list(candidates)
    # Changed waiting plans can first become affordable on an incoming-cash date.
    future_credit_days = sorted({f.day for f in state.flows if f.amount > 0 and
                                request.request_date < f.day <= min(request.horizon, request.desired_completion_date)})
    for day in future_credit_days:
        if day != earliest:
            changed_bases.append(Candidate('wait', (Payment(day, request.requested_amount),), request.requested_amount, full_id))
    for base in changed_bases:
        method = 'full_payment' if base.method == 'wait' else base.method
        if method not in context.profile.payment_methods_user_will_consider:
            continue
        if base.method == 'partial_payment' and not request.allows_partial_payment:
            continue
        candidates.extend(search_changes(base, context, state))
    return candidates


def verify_candidate_plans(candidates: list[Candidate], context: RequestContext,
                           state: Reconstruction, safe: Decimal,
                           earliest: date | None) -> list[CandidateVerification]:
    results = []
    for candidate in candidates:
        errors = validate_candidate(candidate, context, state, safe, earliest)
        payments = candidate.payments
        in_range = bool(payments) and all(context.request.request_date <= p.day <= context.request.horizon and p.amount > 0 for p in payments)
        simulation = simulate(context.request, context.profile, apply_changes(state.flows, candidate.changes), payments) if in_range else None
        checks = {
            'method_accepted': ('full_payment' if candidate.method == 'wait' else candidate.method) in context.profile.payment_methods_user_will_consider,
            'every_payment_possible': bool(simulation and simulation.safe and not state.blocked),
            'full_commitment_completed': not any('partial plan' in e or 'full/wait' in e or 'total' in e or 'installments differ' in e for e in errors),
            'deadline_met': bool(payments) and all(p.day <= context.request.desired_completion_date for p in payments),
            'minimum_maintained': bool(simulation and simulation.safe and not state.blocked),
            'plan_format_valid': in_range and tuple(sorted(payments, key=lambda p: p.day)) == payments,
            'installment_option_matches': not any('option' in e or 'installment' in e or 'stated total' in e for e in errors),
            'spending_changes_valid': not validate_changes(candidate.changes, context, state),
        }
        results.append(CandidateVerification(candidate, checks, tuple(errors), simulation.minimum_balance if simulation else None))
    return results


def rank_valid_plans(verifications: list[CandidateVerification]) -> list[Candidate]:
    return sorted((v.candidate for v in verifications if v.valid), key=rank)


def predict(context: RequestContext, rates: dict[tuple[date, str, str], Decimal]) -> PredictionResult:
    """Backward-compatible entry for existing tests; delegates to the orchestrator."""
    from agent import evaluate_context
    from providers import FakeEvidenceProvider
    return evaluate_context(context, rates, FakeEvidenceProvider()).result
