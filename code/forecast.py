"""Daily cash simulation with intermediate-balance safety checks."""
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, ROUND_FLOOR

from models import CENT, ZERO, CashFlow, Payment, Profile, Request


@dataclass(frozen=True)
class DailyBalance:
    day: date
    opening_balance: Decimal
    credits: Decimal
    essential_debits: Decimal
    other_debits: Decimal
    request_payments: Decimal
    closing_balance: Decimal
    minimum_required: Decimal
    surplus: Decimal
    lowest_balance: Decimal


@dataclass(frozen=True)
class Simulation:
    safe: bool
    minimum_balance: Decimal
    daily_closing: dict[date, Decimal]
    breach_date: date | None
    days: tuple[DailyBalance, ...]
    lowest_balance_date: date


def simulate(request: Request, profile: Profile, flows: list[CashFlow],
             payments: tuple[Payment, ...] = ()) -> Simulation:
    daily: dict[date, list[CashFlow]] = defaultdict(list)
    outgoing: dict[date, list[Payment]] = defaultdict(list)
    for flow in flows:
        if not request.request_date <= flow.day <= request.horizon:
            raise ValueError('flow outside forecast')
        daily[flow.day].append(flow)
    for payment in payments:
        if payment.amount < 0 or not request.request_date <= payment.day <= request.horizon:
            raise ValueError('invalid payment')
        outgoing[payment.day].append(payment)
    balance = profile.current_available_balance
    minimum = balance
    breach = request.request_date if balance < profile.minimum_balance_to_keep else None
    closing = {}
    ledger = []
    lowest_date = request.request_date
    day = request.request_date
    while day <= request.horizon:
        opening = balance
        day_low = balance
        for flow in sorted(daily[day], key=lambda f: (f.amount >= 0, f.source_id)):
            balance += flow.amount
            day_low = min(day_low, balance)
            if balance < minimum:
                lowest_date = day
            minimum = min(minimum, balance)
            if balance < profile.minimum_balance_to_keep and breach is None:
                breach = day
        for payment in outgoing[day]:
            balance -= payment.amount
            day_low = min(day_low, balance)
            if balance < minimum:
                lowest_date = day
            minimum = min(minimum, balance)
            if balance < profile.minimum_balance_to_keep and breach is None:
                breach = day
        closing[day] = balance
        ledger.append(DailyBalance(day, opening,
            sum((f.amount for f in daily[day] if f.amount > 0), ZERO),
            -sum((f.amount for f in daily[day] if f.amount < 0 and (f.essential or f.protected)), ZERO),
            -sum((f.amount for f in daily[day] if f.amount < 0 and not (f.essential or f.protected)), ZERO),
            sum((p.amount for p in outgoing[day]), ZERO), balance, profile.minimum_balance_to_keep,
            balance - profile.minimum_balance_to_keep, day_low))
        day += timedelta(days=1)
    return Simulation(breach is None, minimum, closing, breach, tuple(ledger), lowest_date)


def safe_capacity(request: Request, profile: Profile, flows: list[CashFlow]) -> Decimal:
    baseline = simulate(request, profile, flows)
    if not baseline.safe:
        return ZERO
    # Payment occurs after request-day flows. Later intraday troughs still count.
    lo, hi = 0, int((request.requested_amount / CENT).to_integral_value(rounding=ROUND_FLOOR))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if simulate(request, profile, flows, (Payment(request.request_date, CENT * mid),)).safe:
            lo = mid
        else:
            hi = mid - 1
    return CENT * lo


def earliest_full_payment(request: Request, profile: Profile, flows: list[CashFlow],
                          diagnostics: list[dict] | None = None) -> date | None:
    if not simulate(request, profile, flows).safe:
        if diagnostics is not None:
            diagnostics.append({'reason': 'baseline already breaches minimum; no payment date is safe'})
        return None
    day = request.request_date
    while day <= request.horizon:
        attempt = simulate(request, profile, flows, (Payment(day, request.requested_amount),))
        if diagnostics is not None:
            diagnostics.append({'date': day, 'safe': attempt.safe, 'minimum_balance': attempt.minimum_balance,
                                'breach_date': attempt.breach_date})
        if attempt.safe:
            return day
        day += timedelta(days=1)
    return None
