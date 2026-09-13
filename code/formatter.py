"""Exact challenge columns and deterministic plain decimal formatting."""
from decimal import Decimal

from data_loader import OUTPUT_FIELDS
from models import Decision, Payment


def decimal_text(amount: Decimal) -> str:
    text = format(amount, 'f')
    return text.rstrip('0').rstrip('.') if '.' in text else text


def format_plan(payments: tuple[Payment, ...]) -> str:
    return '|'.join(f'{p.day.isoformat()}:{decimal_text(p.amount)}' for p in payments) or 'none'


def format_decision(decision: Decision) -> dict[str, str]:
    changes = decision.candidate.changes if decision.candidate else ()
    change_text = '|'.join(f'{c.action}:{c.event_id}' + (f':{decimal_text(c.amount)}' if c.amount is not None else '') for c in changes) or 'none'
    return dict(zip(OUTPUT_FIELDS, (
        decision.request_id, decimal_text(decision.safe_amount), decision.status, decision.method,
        format_plan(decision.payments), decision.earliest.isoformat() if decision.earliest else '',
        change_text, decision.explanation), strict=True))
