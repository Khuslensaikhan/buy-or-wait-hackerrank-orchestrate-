"""Compare fixed spending estimators using historical holdouts and public samples.

This is an evaluation tool. Predictions never read these reports or sample labels.
Run: python3.12 code/compare_estimators.py
"""
import json
from collections import defaultdict
from decimal import Decimal, ROUND_CEILING
from statistics import median
from unittest.mock import patch

from config import REPO_ROOT
from data_loader import load_dataset
from evidence import resolve_evidence
from providers import CachedEvidenceProvider, sanitize
from reconstruction import expense_kind, recurring_kind, stream_identity
from sample_evaluation import evaluate


def mean(values):
    return sum(values, Decimal(0)) / len(values)


def quantile(values, fraction):
    values = sorted(values)
    position = (len(values) - 1) * fraction
    index = int(position)
    return values[index] + (values[min(index + 1, len(values) - 1)] - values[index]) * (position - index)


ESTIMATORS = {
    'max_recent3': lambda xs: max(xs[-3:]),
    'mean_recent3': lambda xs: mean(xs[-3:]),
    'median_recent3': lambda xs: median(xs[-3:]),
    'mean_all': mean,
    'median_all': median,
    'q75_all': lambda xs: quantile(xs, Decimal('.75')),
    'upper_mean': lambda xs: max(mean(xs), mean(xs[-3:])),
}


def historical_holdouts(data):
    """Rolling 30-day totals; only transactions preceding the forecast are inputs."""
    provider = CachedEvidenceProvider()
    cases = []
    for request in data.samples:
        context = data.context(request)
        events = resolve_evidence(context, provider).events
        image_ids = {i.related_event_id for i in context.images}
        groups = defaultdict(list)
        for e in events:
            if (e.direction == 'debit' and e.status == 'settled' and e.settlement_date
                    and e.settlement_date <= request.request_date and e.amount is not None
                    and expense_kind(e) == 'variable' and e.event_id not in image_ids):
                groups[stream_identity(e)].append(e)
        for history in groups.values():
            history.sort(key=lambda e: e.settlement_date)
            for split in range(3, len(history)):
                past = history[:split]
                cutoff = past[-1].settlement_date
                if (history[-1].settlement_date - cutoff).days < 30 or recurring_kind(past) is None:
                    continue
                future = [e.amount for e in history[split:] if (e.settlement_date - cutoff).days <= 30]
                if not future:
                    continue
                # Same known cadence/count for every amount estimator.
                cases.append(([e.amount for e in past], len(future), sum(future)))
    return cases


def main():
    data = load_dataset()
    holdouts = historical_holdouts(data)
    results = []
    for name, estimator in ESTIMATORS.items():
        def estimate(history):
            return estimator([e.amount for e in history if e.amount is not None]).quantize(
                Decimal('.01'), rounding=ROUND_CEILING)
        with patch('reconstruction.estimate_debit', estimate):
            report = sanitize(evaluate())
        errors = [(estimator(past) * count - actual) / actual for past, count, actual in holdouts if actual]
        rows = report['rows']
        result = {
            'estimator': name, 'sample_count': report['sample_count'],
            'correct': report['normalized_field_correct'],
            'operational_correct': report['operational_fields_correct'],
            'mean_absolute_error_fraction_of_request': str(mean([
                abs(Decimal(row['actual']['amount_safe_to_pay']) - Decimal(row['expected']['amount_safe_to_pay'])) / req.requested_amount
                for row, req in zip(rows, data.samples, strict=True)])),
            'historical_holdouts': len(errors),
            'historical_mean_absolute_relative_error': str(mean([abs(e) for e in errors])),
            'historical_mean_squared_relative_error': str(mean([e * e for e in errors])),
            'historical_mean_relative_bias': str(mean(errors)),
            'methods': {r['request_id']: r['actual']['recommended_payment_method'] for r in rows},
            'spending_changes': {r['request_id']: r['actual']['spending_changes_needed'] for r in rows},
        }
        results.append(result)
        print(json.dumps({k: v for k, v in result.items() if k not in {'methods', 'spending_changes'}}), flush=True)
    path = REPO_ROOT / 'code/evaluation/estimator_comparison.json'
    path.write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
