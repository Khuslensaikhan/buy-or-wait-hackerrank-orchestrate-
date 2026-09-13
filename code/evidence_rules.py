"""Narrow literal amendment fallback; never parses instructions or decisions."""
import re
from collections import defaultdict
from decimal import Decimal

from evidence_schemas import ExtractedFacts, MessageFact
from models import Message, RequestContext


def literal_amendment(record, context: RequestContext) -> ExtractedFacts | None:
    if not isinstance(record, Message) or record.source_type != 'service_provider':
        return None
    # Whole financial sentences only. No arbitrary commands, evaluated code,
    # invented amounts, source identities, dates, or model-cache entries.
    patterns = (
        r'The renewed lease (increases|decreases) monthly rent by (\d+(?:\.\d+)?)%',
        r'Perpanjangan sewa (menaikkan|menurunkan) biaya sewa bulanan sebesar (\d+(?:\.\d+)?)%',
    )
    matches = []
    for sentence in re.split(r'(?<=[.!?])\s+', record.message_text.strip()):
        for pattern in patterns:
            match = re.fullmatch(pattern + r'\.?', sentence, re.I)
            if match:
                matches.append(match)
    if len(matches) != 1:
        return None
    match = matches[0]
    percentage = Decimal(match[2]) * (-1 if match[1].lower() in {'decreases', 'menurunkan'} else 1)
    if percentage < -100:
        return None
    from reconstruction import add_months, recurring_kind
    groups = defaultdict(list)
    for event in context.events:
        if (event.category == 'rent' and event.direction == 'debit' and event.status == 'settled'
                and event.settlement_date and event.settlement_date <= context.request.request_date):
            groups[(event.description.casefold(), event.currency)].append(event)
    candidates = []
    for history in groups.values():
        history.sort(key=lambda e: e.settlement_date)
        kind = recurring_kind(history)
        if kind and kind[0] == 'monthly' and history[-1].amount is not None:
            day = add_months(history[-1].settlement_date, 1, kind[1])
            if day >= context.request.request_date:
                candidates.append((history[-1], day))
    if len(candidates) != 1:
        return None
    event, day = candidates[0]
    if record.related_event_id and record.related_event_id != event.event_id:
        return None
    return ExtractedFacts(images=[], messages=[MessageFact(
        source_id=record.message_id, related_event_id=event.event_id, confidence=1,
        evidence_summary=f'Literal lease amendment: monthly rent changes by {percentage}% from the next payment.',
        action='amend', new_amount=None, new_currency=None, new_date=day,
        new_status=None, creates_new_event=False, scope='future_recurrence',
        percentage_change=str(percentage))])
