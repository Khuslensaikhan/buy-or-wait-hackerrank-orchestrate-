"""Labels are read only after all sample predictions have completed."""
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from data_loader import (OUTPUT_FIELDS, REPO_ROOT, REQUEST_FIELDS, load_dataset,
                         parse_output, read_rows)
from formatter import format_decision
from planner import predict
from agent import BuyOrWaitAgent
from audit import write_trace
from providers import CachedEvidenceProvider, EvidenceProvider, sanitize


def compare(actual: dict[str, str], expected: dict[str, str]) -> dict[str, bool]:
    """Exact value equality, treating decimal spelling as insignificant."""
    a, e = parse_output(actual), parse_output(expected)
    return {name: getattr(a, name) == getattr(e, name) for name in OUTPUT_FIELDS}


def evaluate(root: Path = REPO_ROOT, provider: EvidenceProvider | None = None, *, audits: bool = False) -> dict:
    data = load_dataset(root)
    agent = BuyOrWaitAgent(data, provider if provider is not None else CachedEvidenceProvider())
    evaluations = [agent.evaluate(request) for request in data.samples]
    results = [evaluation.result for evaluation in evaluations]
    if audits:
        for evaluation in evaluations:
            write_trace(evaluation.trace)
    # The prediction phase has finished. Now, and only now, access expected outputs.
    raw_labels = read_rows(root / 'dataset' / 'sample_requests.csv', REQUEST_FIELDS + OUTPUT_FIELDS[1:])
    labels = {row['request_id']: {k: row[k] for k in OUTPUT_FIELDS} for row in raw_labels}
    rows = []
    for request, result in zip(data.samples, results, strict=True):
        actual = format_decision(result.decision)
        expected = labels[request.request_id]
        context = data.context(request)
        rows.append({
            'request_id': request.request_id,
            'actual': actual, 'expected': expected,
            'matches': compare(actual, expected),
            'exact_text_matches': {k: actual[k] == expected[k] for k in OUTPUT_FIELDS},
            'issues': [asdict(i) for i in result.reconstruction.issues],
            'recurrence': result.reconstruction.recurrence,
            'flows': [asdict(f) for f in result.reconstruction.flows],
            'candidate_rejections': result.rejections,
            'minimum_projected_balance': str(result.minimum_projected_balance),
            'evidence_messages': [asdict(m) for m in context.messages],
            'evidence_images': [asdict(i) for i in context.images],
        })
    total = len(rows)
    operational = tuple(k for k in OUTPUT_FIELDS if k != 'decision_explanation')
    return {
        'sample_count': total,
        'normalized_field_correct': {k: sum(r['matches'][k] for r in rows) for k in OUTPUT_FIELDS},
        'exact_text_field_correct': {k: sum(r['exact_text_matches'][k] for r in rows) for k in OUTPUT_FIELDS},
        'all_fields_correct': sum(all(r['matches'].values()) for r in rows),
        'operational_fields_correct': sum(all(r['matches'][k] for k in operational) for r in rows),
        'exact_text_requests_correct': sum(all(r['exact_text_matches'].values()) for r in rows),
        'dataset_sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted((root / 'dataset').rglob('*')) if p.is_file()},
        'model_usage': agent.provider.usage.report(),
        'rows': rows,
    }


def markdown(report: dict) -> str:
    n = report['sample_count']
    lines = ['# Offline agent sample evaluation', '',
             'Cached evidence only; flexible spending search enabled. Cache misses remain unresolved.',
             'Normalized equality parses decimals and schedules exactly; there is no tolerance.',
             'Explanation accuracy is exact text equality, not semantic grading.', '',
             '| Field | Normalized correct | Exact text correct |',
             '|---|---:|---:|']
    for key in OUTPUT_FIELDS:
        norm = report['normalized_field_correct'][key]
        exact = report['exact_text_field_correct'][key]
        lines.append(f'| {key} | {norm}/{n} ({norm/n:.0%}) | {exact}/{n} ({exact/n:.0%}) |')
    lines.extend(['', f'All fields correct: {report["all_fields_correct"]}/{n}.',
                  f'All operational fields excluding explanation: {report["operational_fields_correct"]}/{n}.',
                  f'Exact-text full rows: {report["exact_text_requests_correct"]}/{n}.', '',
                  '## Mismatch table', '',
                  '| Request | Safe amount: predicted / expected | Method: predicted / expected | Incorrect fields |',
                  '|---|---|---|---|'])
    abbreviations = dict(zip(OUTPUT_FIELDS, ('ID', 'A', 'S', 'M', 'P', 'D', 'C', 'E'), strict=True))
    for row in report['rows']:
        if all(row['matches'].values()):
            continue
        a, e = row['actual'], row['expected']
        bad = ', '.join(abbreviations[k] for k in OUTPUT_FIELDS if not row['matches'][k])
        lines.append(f'| {row["request_id"]} | {a["amount_safe_to_pay"]} / {e["amount_safe_to_pay"]} | '
                     f'{a["recommended_payment_method"]} / {e["recommended_payment_method"]} | {bad} |')
    lines.extend(['', 'A=safe amount; S=status; M=method; P=plan; D=earliest date; C=spending changes; E=explanation.', '',
                  '## Detailed diagnostics', ''])
    for row in report['rows']:
        lines.extend([f'### {row["request_id"]}', ''])
        for key in OUTPUT_FIELDS:
            if not row['matches'][key]:
                lines.extend([f'* {key}:', f'  * predicted: `{row["actual"][key]}`',
                              f'  * expected: `{row["expected"][key]}`'])
        lines.extend(['', f'Minimum projected balance: {row["minimum_projected_balance"]}', '', 'Evidence/issues:'])
        lines.extend(f'* {i["code"]} {i["source_id"]}: {i["detail"]}; blocking={i["blocking"]}' for i in row['issues'])
        lines.extend(['', 'Candidate rejections:'])
        lines.extend(f'* {r}' for r in row['candidate_rejections'])
        lines.extend(['', 'Inferred streams:'])
        lines.extend(f'* {r}' for r in row['recurrence'])
        lines.append('')
    return '\n'.join(lines) + '\n'


def run_evaluation() -> None:
    report = sanitize(evaluate(audits=True))
    folder = REPO_ROOT / 'code' / 'evaluation'
    folder.mkdir(parents=True, exist_ok=True)
    content = markdown(report)
    (folder / 'sample_results.json').write_text(json.dumps(report, indent=2, default=str) + '\n', encoding='utf-8')
    (folder / 'sample_results.md').write_text(content, encoding='utf-8')
    print(content)
