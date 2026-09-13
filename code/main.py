"""Terminal commands. Only extract-evidence --live can create a live provider."""
import argparse
import csv
import json
import sys
from decimal import Decimal
from pathlib import Path

from agent import BuyOrWaitAgent
from audit import trace_markdown, write_trace
from config import REPO_ROOT
from data_loader import OUTPUT_FIELDS, load_dataset, read_rows
from evidence import resolve_evidence
from output_validation import validate_row, verify_output_row
from providers import CachedEvidenceProvider, OpenAIEvidenceProvider, sanitize
from sample_evaluation import run_evaluation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Buy or Wait — offline by default')
    commands = parser.add_subparsers(dest='command', required=True)
    evaluation = commands.add_parser('evaluate-samples')
    evaluation.add_argument('--offline', action='store_true', help='Default; cache only')
    trace = commands.add_parser('trace')
    group = trace.add_mutually_exclusive_group(required=True)
    group.add_argument('--sample')
    group.add_argument('--request')
    trace.add_argument('--offline', action='store_true')
    extract = commands.add_parser('extract-evidence')
    group = extract.add_mutually_exclusive_group(required=True)
    group.add_argument('--samples', action='store_true')
    group.add_argument('--all', action='store_true')
    extract.add_argument('--live', action='store_true', help='Explicitly permit billable extraction on cache misses')
    prediction = commands.add_parser('predict')
    prediction.add_argument('--offline', action='store_true', help='Default; never silently calls OpenAI')
    prediction.add_argument('--output', type=Path, required=True)
    validation = commands.add_parser('validate-output')
    validation.add_argument('output', type=Path)
    return parser


def repo_path(path: Path) -> Path:
    return (path if path.is_absolute() else REPO_ROOT / path).resolve()


def write_predictions(agent: BuyOrWaitAgent, output: Path) -> int:
    output = repo_path(output)
    if output.is_relative_to((REPO_ROOT / 'dataset').resolve()):
        raise ValueError('dataset is read-only')
    rows = []
    for request in agent.dataset.requests:
        evaluation = agent.evaluate(request)
        errors = validate_row(evaluation.row, request)
        if errors:
            raise ValueError(f'{request.request_id}: invalid generated row: {errors}')
        rows.append(evaluation.row)
        write_trace(evaluation.trace)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + '.tmp')
    with temporary.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(output)
    write_usage(agent.provider, len(rows), 'full-dataset prediction')
    return len(rows)


def write_usage(provider, count: int, run_kind: str) -> None:
    folder = REPO_ROOT / 'code' / 'evaluation'
    folder.mkdir(parents=True, exist_ok=True)
    usage = provider.usage.report()
    usage.update(requests=count, run_kind=run_kind,
                 total_tokens=provider.usage.input_tokens + provider.usage.output_tokens)
    usage['average_tokens_per_request'] = str(Decimal(usage['total_tokens']) / count) if count else '0'
    usage['estimated_cost_per_request'] = (str(Decimal(usage['estimated_cost']) / count)
                                            if count and usage['estimated_cost'] is not None else None)
    content = json.dumps(sanitize(usage), indent=2, default=str)
    (folder / 'usage_report.json').write_text(content + '\n')
    (folder / 'usage_report.md').write_text('# Run usage\n\n```json\n' + content + '\n```\n')


def main(argv: list[str] | None = None) -> int:
    if sys.version_info[:2] != (3, 12):
        raise SystemExit('Use Python 3.12.')
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == 'evaluate-samples':
            run_evaluation()
            return 0
        data = load_dataset()
        if args.command == 'extract-evidence':
            fallback = OpenAIEvidenceProvider(live=True) if args.live else None
            provider = CachedEvidenceProvider(fallback=fallback)
            requests = data.samples if args.samples else data.samples + data.requests
            records = []
            for request in requests:
                resolution = resolve_evidence(data.context(request), provider)
                records.append({'request_id': request.request_id, 'used': resolution.used,
                                'skipped': resolution.skipped,
                                'issues': [vars(i) for i in resolution.issues]})
            report = sanitize({'usage': provider.usage.report(), 'requests': records})
            folder = REPO_ROOT / 'code' / 'evaluation'
            folder.mkdir(parents=True, exist_ok=True)
            (folder / 'evidence_extraction.json').write_text(json.dumps(report, indent=2, default=str) + '\n')
            print(json.dumps(report, indent=2, default=str))
            write_usage(provider, len(requests), 'evidence extraction only; no predictions')
            return 0
        agent = BuyOrWaitAgent(data, CachedEvidenceProvider())
        if args.command == 'trace':
            requests = data.samples if args.sample else data.requests
            identity = args.sample or args.request
            request = next((r for r in requests if r.request_id == identity), None)
            if request is None:
                raise ValueError('unknown request ID in selected split')
            evaluation = agent.evaluate(request)
            write_trace(evaluation.trace)
            print(trace_markdown(sanitize(evaluation.trace)))
            return 0
        if args.command == 'predict':
            count = write_predictions(agent, args.output)
            print(f'Wrote {count} offline predictions to {repo_path(args.output)}')
            return 0
        if args.command == 'validate-output':
            rows = read_rows(repo_path(args.output), OUTPUT_FIELDS)
            by_id = {r.request_id: r for r in data.requests}
            seen = set()
            errors = []
            for row in rows:
                identity = row['request_id']
                if identity in seen or identity not in by_id:
                    errors.append(f'{identity}: duplicate or unknown request')
                    continue
                seen.add(identity)
                errors.extend(f'{identity}: {e}' for e in verify_output_row(row, by_id[identity], agent))
            errors.extend(f'{identity}: missing output row' for identity in sorted(set(by_id) - seen))
            print('\n'.join(errors) if errors else f'Validated all {len(rows)} rows against the offline engine.')
            return 1 if errors else 0
    except (ValueError, OSError) as exc:
        print(sanitize(f'{type(exc).__name__}: {exc}'), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
