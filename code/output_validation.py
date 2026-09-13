"""Output contract validation, optionally re-verifying against the offline engine."""
from dataclasses import replace
from decimal import Decimal

from data_loader import OUTPUT_FIELDS, parse_output
from models import Candidate, Request, RequestContext
from planner import validate_candidate

STATUSES = {'affordable_now', 'affordable_with_plan', 'affordable_later', 'not_affordable'}
METHODS = {'full_payment', 'partial_payment', 'installments', 'wait', 'not_recommended'}


def validate_row(row: dict[str, str], request: Request) -> list[str]:
    errors = []
    if tuple(row) != OUTPUT_FIELDS:
        errors.append('incorrect output schema or column order')
    if any(k not in row for k in OUTPUT_FIELDS):
        return errors
    if row['request_id'] != request.request_id:
        errors.append('request identity mismatch')
    if row['affordability_status'] not in STATUSES or row['recommended_payment_method'] not in METHODS:
        errors.append('invalid output enum')
    try:
        output = parse_output(row)
    except (ValueError, ArithmeticError):
        return errors + ['malformed money, plan, date or changes']
    if output.amount_safe_to_pay is None or not Decimal('0') <= output.amount_safe_to_pay <= request.requested_amount:
        errors.append('safe amount out of bounds or missing')
    if not row['decision_explanation'].strip():
        errors.append('missing explanation')
    if not row['payment_plan'] or not row['spending_changes_needed']:
        errors.append('use none, not blank, for absent plans/changes')
    payments = output.payment_plan
    if tuple(sorted(payments, key=lambda p: p.day)) != payments:
        errors.append('nonchronological payments')
    if any(p.amount <= 0 or p.day < request.request_date or p.day > min(request.desired_completion_date, request.horizon) for p in payments):
        errors.append('payment violates amount/date/deadline bounds')
    if len(output.spending_changes_needed) > 3 or len({c.event_id for c in output.spending_changes_needed}) != len(output.spending_changes_needed):
        errors.append('too many or conflicting spending changes')
    if output.earliest_date_for_full_payment and not request.request_date <= output.earliest_date_for_full_payment <= request.horizon:
        errors.append('earliest date outside forecast')
    method, status = output.recommended_payment_method, output.affordability_status
    expected_status = ('not_affordable' if method == 'not_recommended' else
                       'affordable_with_plan' if output.spending_changes_needed or method in {'partial_payment', 'installments'} else
                       'affordable_now' if method == 'full_payment' else 'affordable_later')
    if status != expected_status:
        errors.append('status does not match selected method and changes')
    if method == 'not_recommended':
        if status != 'not_affordable' or payments or output.spending_changes_needed:
            errors.append('rejection must have not_affordable and no plan/changes')
    elif not payments:
        errors.append('selected method requires a payment plan')
    if status == 'affordable_now' and (method != 'full_payment' or output.spending_changes_needed or output.earliest_date_for_full_payment != request.request_date):
        errors.append('invalid affordable_now mapping')
    if method in {'partial_payment', 'installments'} and status != 'affordable_with_plan':
        errors.append('scheduled commitment must be affordable_with_plan')
    if output.spending_changes_needed and status != 'affordable_with_plan':
        errors.append('spending changes require affordable_with_plan')
    if method == 'wait' and not output.spending_changes_needed and status != 'affordable_later':
        errors.append('waiting without changes requires affordable_later')
    if method == 'partial_payment':
        if not request.allows_partial_payment or not output.amount_safe_to_pay or not output.amount_safe_to_pay < request.requested_amount:
            errors.append('partial payment ineligible')
        if len(payments) != 2 or sum((p.amount for p in payments), Decimal('0')) != request.requested_amount:
            errors.append('partial plan must have two payments summing to principal')
        elif payments[0].day != request.request_date or payments[0].amount != output.amount_safe_to_pay or payments[1].day != output.earliest_date_for_full_payment:
            errors.append('partial plan violates baseline dates/amount')
    return errors


def verify_output_row(row: dict[str, str], request: Request, agent) -> list[str]:
    errors = validate_row(row, request)
    if errors:
        return errors
    evaluation = agent.evaluate(request)
    expected = evaluation.result.decision
    output = parse_output(row)
    if output.amount_safe_to_pay != expected.safe_amount:
        errors.append('safe amount differs from reconstructed baseline')
    if output.earliest_date_for_full_payment != expected.earliest:
        errors.append('earliest date differs from reconstructed baseline')
    if output.recommended_payment_method == 'not_recommended':
        if expected.candidate:
            errors.append('a safe eligible candidate exists')
        return errors
    context = replace(agent.load_request_context(request), events=evaluation.result.reconstruction.resolved_events)
    option_id = ''
    total = request.requested_amount
    if output.recommended_payment_method == 'installments':
        matches = [o for o in context.options if o.payment_method == 'installments' and o.payments() == output.payment_plan]
        if not matches:
            return errors + ['installments do not match a supplied option']
        option = min(matches, key=lambda o: o.payment_option_id)
        option_id, total = option.payment_option_id, option.total_payable_amount
    candidate = Candidate(output.recommended_payment_method, output.payment_plan, total, option_id, output.spending_changes_needed)
    errors.extend(validate_candidate(candidate, context, evaluation.result.reconstruction, expected.safe_amount, expected.earliest))
    if expected.candidate and (candidate.method, candidate.payments, candidate.changes) != (
            expected.candidate.method, expected.candidate.payments, expected.candidate.changes):
        errors.append('row does not match highest-ranked deterministic candidate')
    return errors
