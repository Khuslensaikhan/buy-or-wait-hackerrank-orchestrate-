"""Resumable extraction of a globally deduplicated, deterministic source queue."""
import json
from dataclasses import dataclass, field
from pathlib import Path
from time import monotonic
from typing import Iterable

from models import ImageEvidence, Message, RequestContext
from providers import CachedEvidenceProvider, EvidenceUnavailable, atomic_json_write, sanitize, source_for


@dataclass
class ExtractionItem:
    record: Message | ImageEvidence
    context: RequestContext
    request_ids: list[str] = field(default_factory=list)

    @property
    def source_id(self) -> str:
        return self.record.message_id if isinstance(self.record, Message) else self.record.image_id

    @property
    def kind(self) -> str:
        return 'message' if isinstance(self.record, Message) else 'image'


def collect_evidence(contexts: Iterable[RequestContext], *, limit: int | None = None,
                     source_id: str | None = None) -> list[ExtractionItem]:
    """First referring context is canonical; never mix evidence across users."""
    unique: dict[tuple[str, str], ExtractionItem] = {}
    for context in contexts:
        for record in (*context.images, *context.messages):
            item = ExtractionItem(record, context, [context.request.request_id])
            key = (item.kind, item.source_id)
            if key in unique:
                previous = unique[key]
                if previous.record != record or previous.context.request.user_id != context.request.user_id:
                    raise ValueError(f'conflicting evidence identity: {item.source_id}')
                if context.request.request_id not in previous.request_ids:
                    previous.request_ids.append(context.request.request_id)
            else:
                unique[key] = item
    items = list(unique.values())
    if source_id is not None:
        items = [item for item in items if item.source_id == source_id]
        if not items:
            raise ValueError('unknown source ID in selected request scope')
    if limit is not None:
        if limit < 0:
            raise ValueError('limit must be nonnegative')
        items = items[:limit]
    return items


def dry_run_summary(items: list[ExtractionItem], provider: CachedEvidenceProvider,
                    max_retries: int = 1) -> dict:
    cached = missing = 0
    errors = []
    for item in items:
        try:
            if provider.lookup(source_for(item.record), item.context) is not None:
                cached += 1
            else:
                missing += 1
        except (ValueError, OSError) as exc:
            errors.append({'source_id': item.source_id, **error_details(exc)})
    return {'unique_messages': sum(i.kind == 'message' for i in items),
            'unique_images': sum(i.kind == 'image' for i in items),
            'already_cached': cached, 'requiring_live_calls': missing,
            'estimated_call_count': missing, 'maximum_http_attempts': missing * (1 + max_retries),
            'evidence_ids_in_processing_order': [i.source_id for i in items],
            'unavailable_sources': errors}


def error_details(exc: Exception) -> dict:
    # SDK bodies may echo arbitrary sensitive input; fixed diagnostics are safer.
    category = getattr(exc, 'error_type', type(exc).__name__)
    detail = str(exc) if isinstance(exc, EvidenceUnavailable) else f'evidence processing failed ({category})'
    return {'error_type': category, 'sanitized_message': sanitize(detail).replace('\n', ' ').replace('\r', ' ')}


def run_extraction(items: list[ExtractionItem], provider: CachedEvidenceProvider,
                   audit_dir: Path) -> dict:
    records: list[dict] = []
    interrupted = False
    current = None
    try:
        for index, item in enumerate(items, 1):
            current = {'source_id': item.source_id, 'source_type': item.kind,
                       'related_event_id': item.record.related_event_id, 'request_ids': item.request_ids}
            prefix = f'[{index}/{len(items)}]'
            start = monotonic()
            before = (provider.usage.input_tokens, provider.usage.output_tokens)
            try:
                source = source_for(item.record)
                cached = provider.lookup(source, item.context)
                if cached is not None:
                    provider.usage.cached_resolutions += 1
                    current['status'] = 'CACHE_HIT'
                    print(f'{prefix} CACHE_HIT {item.source_id}', flush=True)
                else:
                    if provider.fallback is not None:
                        print(f'{prefix} START {item.kind} {item.source_id} '
                              f'{item.record.related_event_id or "none"}', flush=True)
                    provider.resolve(source, item.context)  # Commits before next source or DONE.
                    current['status'] = 'DONE'
                current.update(duration_seconds=round(monotonic() - start, 3),
                               input_tokens=provider.usage.input_tokens - before[0],
                               output_tokens=provider.usage.output_tokens - before[1])
                print(f'{prefix} DONE {item.source_id} {current["duration_seconds"]:.3f} '
                      f'{current["input_tokens"]} {current["output_tokens"]}', flush=True)
            except Exception as exc:
                current.update(status='ERROR', **error_details(exc))
                print(f'{prefix} ERROR {item.source_id} {current["error_type"]} '
                      f'{current["sanitized_message"]}', flush=True)
            records.append(current)
            current = None
    except KeyboardInterrupt:
        interrupted = True
        if current is not None:
            # An interruption during the atomic commit can still have saved this result.
            try:
                saved = provider.lookup(source_for(item.record), item.context) is not None
            except (ValueError, OSError):
                saved = False
            current.update(status='DONE' if saved else 'INTERRUPTED', interrupted=True)
            records.append(current)
        print('INTERRUPTED: completed cache entries are preserved.', flush=True)
    finally:
        summary = {'selected': len(items), 'completed': sum(r['status'] == 'DONE' for r in records),
                   'cached': sum(r['status'] == 'CACHE_HIT' for r in records),
                   'failed': sum(r['status'] == 'ERROR' for r in records),
                   'interrupted': interrupted, 'unprocessed': len(items) - len(records)}
        report = sanitize({'summary': summary, 'usage': provider.usage.report(), 'sources': records})
        print('SUMMARY ' + json.dumps(summary), flush=True)
        atomic_json_write(audit_dir / 'evidence_extraction.json', report)
        (audit_dir / 'evidence_extraction.md').write_text(
            '# Evidence extraction audit\n\n```json\n' + json.dumps(report, indent=2, default=str) + '\n```\n',
            encoding='utf-8')
    return report
