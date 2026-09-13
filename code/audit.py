"""Secret-redacted Markdown and JSON traces; no raw image bytes or credentials."""
import json
import re
from pathlib import Path

from config import REPO_ROOT
from providers import sanitize


def trace_markdown(trace: dict) -> str:
    lines = [f'# Trace: {trace["request_id"]}', '', '## Retrieved context', '',
             json.dumps(trace['context_counts'], default=str), '', '## Evidence', '']
    lines.extend(f'* Used: {json.dumps(item, default=str)}' for item in trace['evidence_used'])
    lines.extend(f'* Skipped: {json.dumps(item, default=str)}' for item in trace['evidence_skipped'])
    lines.extend(f'* Issue: {json.dumps(item, default=str)}' for item in trace['issues'])
    lines.extend(['', '## Resolved events', '', '| Event | Date | Amount | Currency | Status | Evidence |', '|---|---|---:|---|---|---|'])
    for e in trace['resolved_events']:
        lines.append(f'| {e["event_id"]} | {e["settlement_date"]} | {e["amount"]} | {e["currency"]} | {e["status"]} | {", ".join(e["evidence_ids"])} |')
    lines.extend(['', '## Projected recurrence', ''])
    lines.extend(f'* {r}' for r in trace['projected_recurrence'])
    lines.extend(['', '## Capacity', '', f'Baseline minimum: {trace["baseline_minimum_balance"]} on {trace["baseline_lowest_date"]}.',
                  json.dumps(trace['amount_safe_calculation'], default=str), '', '## Earliest full-payment tests', ''])
    lines.extend(f'* {json.dumps(t, default=str)}' for t in trace['earliest_full_payment_tests'])
    lines.extend(['', '## Every candidate', ''])
    for i, c in enumerate(trace['candidates'], 1):
        lines.extend([f'### Candidate {i}', '', '```json', json.dumps(c, indent=2, default=str), '```', ''])
    lines.extend(['## Selected recommendation', '', '```json', json.dumps(trace['output_row'], indent=2), '```', '',
                  '## Daily selected forecast', '',
                  '| Date | Opening | Credits | Essential/protected debits | Other debits | Request payments | Closing | Required | Surplus | Lowest |',
                  '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|'])
    for d in trace['selected_daily']:
        lines.append('| ' + ' | '.join(str(d[k]) for k in ('day', 'opening_balance', 'credits', 'essential_debits', 'other_debits',
                                                            'request_payments', 'closing_balance', 'minimum_required', 'surplus', 'lowest_balance')) + ' |')
    return '\n'.join(lines) + '\n'


def write_trace(trace: dict, folder: Path | None = None) -> tuple[Path, Path]:
    folder = folder or REPO_ROOT / 'code' / 'evaluation' / 'traces'
    identity = trace['request_id']
    if not re.fullmatch(r'[A-Za-z0-9_-]+', identity):
        raise ValueError('unsafe request identifier for trace filename')
    folder.mkdir(parents=True, exist_ok=True)
    clean = sanitize(trace)
    js, md = folder / f'{identity}.json', folder / f'{identity}.md'
    js.write_text(json.dumps(clean, indent=2, default=str) + '\n', encoding='utf-8')
    md.write_text(trace_markdown(clean), encoding='utf-8')
    return js, md
