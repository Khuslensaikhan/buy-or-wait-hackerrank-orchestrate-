"""Typed domain records. Requests intentionally cannot carry evaluation labels."""
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

ZERO = Decimal('0')
CENT = Decimal('0.01')


@dataclass(frozen=True)
class Profile:
    user_id: str
    home_currency: str
    current_available_balance: Decimal
    minimum_balance_to_keep: Decimal
    financial_priorities: frozenset[str]
    expense_categories_to_protect: frozenset[str]
    expense_categories_user_is_willing_to_reduce: frozenset[str]
    expense_categories_user_is_willing_to_stop: frozenset[str]
    payment_methods_user_will_consider: frozenset[str]
    max_installment_months: int | None


@dataclass(frozen=True)
class Request:
    request_id: str
    user_id: str
    request_date: date
    request_type: str
    requested_amount: Decimal
    desired_completion_date: date
    allows_partial_payment: bool
    request_text: str

    @property
    def horizon(self) -> date:
        return self.request_date + timedelta(days=90)


@dataclass(frozen=True)
class Event:
    event_id: str
    user_id: str
    event_type: str
    description: str
    category: str
    direction: str
    amount: Decimal | None
    currency: str
    event_date: date
    settlement_date: date | None
    status: str
    linked_event_id: str | None
    flexibility: str
    minimum_allowed_amount: Decimal | None
    evidence_ids: tuple[str, ...] = field(default=(), metadata={'csv': False})
    recurrence_override_amount: Decimal | None = field(default=None, metadata={'csv': False})
    recurrence_override_date: date | None = field(default=None, metadata={'csv': False})
    recurrence_override_currency: str | None = field(default=None, metadata={'csv': False})
    recurrence_override_day: int | None = field(default=None, metadata={'csv': False})
    recurrence_cancelled: bool = field(default=False, metadata={'csv': False})
    recurrence_reason: str = field(default='', metadata={'csv': False})


@dataclass(frozen=True)
class ExchangeRate:
    rate_date: date
    from_currency: str
    to_currency: str
    rate: Decimal


@dataclass(frozen=True, order=True)
class Payment:
    day: date
    amount: Decimal


@dataclass(frozen=True)
class PaymentOption:
    payment_option_id: str
    request_id: str
    payment_method: str
    payment_amount: Decimal
    number_of_payments: int
    first_payment_date: date
    payment_frequency_days: int | None
    financing_fee: Decimal
    total_payable_amount: Decimal

    def payments(self) -> tuple[Payment, ...]:
        if self.number_of_payments < 1:
            raise ValueError('payment count must be positive')
        if self.number_of_payments > 1 and (self.payment_frequency_days or 0) <= 0:
            raise ValueError('multiple payments require a positive interval')
        return tuple(Payment(self.first_payment_date + timedelta(
            days=i * (self.payment_frequency_days or 0)), self.payment_amount)
            for i in range(self.number_of_payments))


@dataclass(frozen=True)
class Message:
    message_id: str
    user_id: str
    request_id: str | None
    related_event_id: str | None
    sent_at: datetime
    source_type: str
    message_text: str


@dataclass(frozen=True)
class ImageEvidence:
    image_id: str
    user_id: str
    request_id: str | None
    related_event_id: str | None
    path: Path


@dataclass(frozen=True)
class SpendingChange:
    action: str
    event_id: str
    amount: Decimal | None = None


@dataclass(frozen=True)
class OutputRecord:
    """Typed solved row or blank template; never passed into the engine."""
    request_id: str
    amount_safe_to_pay: Decimal | None
    affordability_status: str | None
    recommended_payment_method: str | None
    payment_plan: tuple[Payment, ...]
    earliest_date_for_full_payment: date | None
    spending_changes_needed: tuple[SpendingChange, ...]
    decision_explanation: str


@dataclass(frozen=True)
class RequestContext:
    request: Request
    profile: Profile
    events: tuple[Event, ...]
    options: tuple[PaymentOption, ...]
    messages: tuple[Message, ...]
    images: tuple[ImageEvidence, ...]
    rates: dict[tuple[date, str, str], Decimal] = field(default_factory=dict)


@dataclass(frozen=True)
class Issue:
    code: str
    source_id: str
    detail: str
    blocking: bool = False


@dataclass(frozen=True)
class CashFlow:
    day: date
    amount: Decimal  # Signed home-currency amount.
    source_id: str
    inferred: bool = False
    direction: str = ''
    classification: str = 'original'
    essential: bool = False
    protected: bool = False
    flexibility: str = 'fixed'
    recurrence_reason: str = ''
    evidence_ids: tuple[str, ...] = ()
    original_amount: Decimal | None = None
    original_currency: str = ''
    conversion_rate: Decimal = Decimal('1')


@dataclass
class Reconstruction:
    flows: list[CashFlow] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)
    recurrence: list[str] = field(default_factory=list)
    resolved_events: tuple[Event, ...] = ()

    @property
    def blocked(self) -> bool:
        return any(issue.blocking for issue in self.issues)


@dataclass(frozen=True)
class Candidate:
    method: str
    payments: tuple[Payment, ...]
    total_cost: Decimal
    option_id: str = ''
    changes: tuple[SpendingChange, ...] = ()
    change_reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class Decision:
    request_id: str
    safe_amount: Decimal
    status: str
    method: str
    payments: tuple[Payment, ...]
    earliest: date | None
    explanation: str
    candidate: Candidate | None


@dataclass
class PredictionResult:
    decision: Decision
    reconstruction: Reconstruction
    rejections: list[str]
    minimum_projected_balance: Decimal
