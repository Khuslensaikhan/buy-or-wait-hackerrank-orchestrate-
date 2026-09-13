"""The seven-stage Buy or Wait orchestrator. Evidence providers never decide money."""
from dataclasses import asdict, dataclass, replace
from datetime import date
from decimal import Decimal

from data_loader import Dataset, load_dataset
from evidence import EvidenceResolution, resolve_evidence
from forecast import earliest_full_payment, safe_capacity, simulate
from formatter import format_decision
from models import ZERO, Decision, Payment, PredictionResult, Request, RequestContext
from planner import generate_candidate_plans, rank, rank_valid_plans, verify_candidate_plans
from providers import CachedEvidenceProvider, EvidenceProvider
from reconstruction import reconstruct
from spending import apply_changes


@dataclass
class AgentEvaluation:
    row: dict[str, str]
    result: PredictionResult
    trace: dict


def generate_grounded_explanation(context, state, safe, earliest, chosen, final, verifications) -> str:
    profile = context.profile
    text = f'Safe today before changes: {safe} {profile.home_currency}; protected minimum: {profile.minimum_balance_to_keep}. '
    if chosen:
        text += (f'Use {chosen.method}, total {chosen.total_cost}, completing {chosen.payments[-1].day}. '
                 f'Lowest projected balance: {final.minimum_balance} on {final.lowest_balance_date}. ')
        if chosen.changes:
            text += 'Required changes: ' + '; '.join(f'{c.action}:{c.event_id}' +
                (f':{c.amount}' if c.amount is not None else '') for c in chosen.changes) + '. '
        if chosen.method == 'wait':
            text += 'Earlier full payment would not preserve the reserve under this forecast. '
    else:
        text += 'No safe eligible plan completes by the deadline under the resolved forecast. '
        if earliest and earliest > context.request.desired_completion_date:
            text += f'Baseline full payment first becomes safe on {earliest}, after the deadline. '
        if verifications and all(not v.checks['method_accepted'] for v in verifications):
            text += 'Available methods are excluded by the user. '
    limiting = [f for f in state.flows if f.day == final.lowest_balance_date and f.amount < 0]
    if limiting:
        largest = min(limiting, key=lambda f: f.amount)
        text += f'Limiting expense: {largest.source_id} ({-largest.amount} on {largest.day}). '
    if chosen and chosen.method in {'wait', 'partial_payment', 'installments'}:
        funding = [f for f in state.flows if f.amount > 0 and f.day <= chosen.payments[-1].day]
        if funding:
            first = min(funding, key=lambda f: (f.day, f.source_id))
            text += f'Projected income includes {first.source_id}: {first.amount} on {first.day}. '
    if state.issues:
        text += 'Unresolved evidence/forecast assumptions remain; see audit. '
    if state.blocked:
        text += 'Zero capacity is an uncertified fallback for missing required financial facts.'
    return text.strip()


def evaluate_context(context: RequestContext, rates: dict[tuple[date, str, str], Decimal],
                     provider: EvidenceProvider, stages=None) -> AgentEvaluation:
    """Run the same stages for integration fixtures and loaded requests."""
    stages = stages or BuyOrWaitAgent
    resolution = stages.resolve_evidence(context, provider)
    resolved_context = replace(context, events=resolution.events)
    state = stages.reconstruct_events(resolved_context, rates, evidence_issues=resolution.issues)
    baseline = stages.build_baseline_forecast(context.request, context.profile, state.flows)
    safe = ZERO if state.blocked else stages.calculate_amount_safe_today(context.request, context.profile, state.flows)
    safe_test = simulate(context.request, context.profile, state.flows, (Payment(context.request.request_date, safe),))
    earliest_tests: list[dict] = []
    earliest = None if state.blocked else stages.calculate_earliest_full_payment_date(context.request, context.profile, state.flows, earliest_tests)
    candidates = stages.generate_candidate_plans(resolved_context, state, safe, earliest)
    verifications = stages.verify_candidate_plans(candidates, resolved_context, state, safe, earliest)
    valid = stages.rank_valid_plans(verifications)
    chosen = valid[0] if valid else None
    selected_flows = apply_changes(state.flows, chosen.changes) if chosen else state.flows
    final = simulate(context.request, context.profile, selected_flows, chosen.payments if chosen else ())
    status = 'not_affordable'
    if chosen:
        status = 'affordable_with_plan' if chosen.changes or chosen.method in {'partial_payment', 'installments'} else (
            'affordable_now' if chosen.method == 'full_payment' else 'affordable_later')
    explanation = stages.generate_grounded_explanation(context, state, safe, earliest, chosen, final, verifications)
    decision = Decision(context.request.request_id, safe, status, chosen.method if chosen else 'not_recommended',
                        chosen.payments if chosen else (), earliest, explanation, chosen)
    rejections = [f'{v.candidate.method} {v.candidate.option_id}: ' + '; '.join(v.errors) for v in verifications if not v.valid]
    result = PredictionResult(decision, state, rejections, final.minimum_balance)
    trace = {
        'architecture': ['Input Request', 'Retrieve Context', 'Reconstruct Financial Reality',
                         'Build 90-Day Baseline', 'Generate Payment Candidates', 'Verify and Rank', 'Produce output row'],
        'request_id': context.request.request_id,
        'context_counts': {'events': len(context.events), 'messages': len(context.messages), 'images': len(context.images),
                           'options': len(context.options), 'exchange_rates': len(rates)},
        'evidence_used': resolution.used, 'evidence_skipped': resolution.skipped,
        'issues': [asdict(i) for i in state.issues],
        'resolved_events': [asdict(e) for e in state.resolved_events],
        'projected_recurrence': state.recurrence,
        'cash_flows': [asdict(f) for f in state.flows],
        'baseline_daily': [asdict(d) for d in baseline.days],
        'baseline_lowest_date': baseline.lowest_balance_date,
        'baseline_minimum_balance': baseline.minimum_balance,
        'amount_safe_calculation': {'amount': safe, 'verified_by_simulation': safe_test.safe and not state.blocked,
                                    'blocked': state.blocked, 'algorithm': 'maximum cent amount via monotone binary search'},
        'earliest_full_payment_tests': earliest_tests,
        'candidates': [{'candidate': asdict(v.candidate), 'checks': v.checks, 'errors': v.errors,
                        'valid': v.valid, 'minimum_balance': v.minimum_balance,
                        'ranking_key': rank(v.candidate) if v.valid else None} for v in verifications],
        'selected': asdict(chosen) if chosen else None,
        'selected_daily': [asdict(d) for d in final.days],
        'selected_lowest_date': final.lowest_balance_date,
        'usage': provider.usage.report(),
    }
    row = stages.format_output_row(decision)
    trace['output_row'] = row
    return AgentEvaluation(row, result, trace)


class BuyOrWaitAgent:
    resolve_evidence = staticmethod(resolve_evidence)
    reconstruct_events = staticmethod(reconstruct)
    build_baseline_forecast = staticmethod(simulate)
    calculate_amount_safe_today = staticmethod(safe_capacity)
    calculate_earliest_full_payment_date = staticmethod(earliest_full_payment)
    generate_candidate_plans = staticmethod(generate_candidate_plans)
    verify_candidate_plans = staticmethod(verify_candidate_plans)
    rank_valid_plans = staticmethod(rank_valid_plans)
    generate_grounded_explanation = staticmethod(generate_grounded_explanation)
    format_output_row = staticmethod(format_decision)

    def __init__(self, dataset: Dataset | None = None, provider: EvidenceProvider | None = None):
        self.dataset = dataset if dataset is not None else load_dataset()
        self.provider = provider if provider is not None else CachedEvidenceProvider()

    def load_request_context(self, request: Request) -> RequestContext:
        return self.dataset.context(request)

    def evaluate(self, request: Request) -> AgentEvaluation:
        context = self.load_request_context(request)
        return evaluate_context(context, context.rates, self.provider, stages=self)
