"""Extraction schemas contain facts only, never balances, decisions or schedules."""
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Status = Literal['settled', 'pending', 'scheduled', 'failed', 'cancelled', 'unrealized']
Direction = Literal['debit', 'credit', 'non_cash']


class Fact(BaseModel):
    model_config = ConfigDict(extra='forbid')
    source_id: str
    related_event_id: str | None
    confidence: float = Field(ge=0, le=1)
    evidence_summary: str


def checked_amount(value: str | None) -> str | None:
    if value is not None:
        try:
            number = Decimal(value)
        except InvalidOperation:
            raise ValueError('invalid decimal amount') from None
        if not number.is_finite() or number < 0:
            raise ValueError('amount must be a nonnegative decimal string or null')
    return value


class ImageFact(Fact):
    document_type: str | None
    amount: str | None
    currency: str | None
    effective_date: date | None
    status: Status | None
    direction: Direction | None

    _amount = field_validator('amount')(checked_amount)


class MessageFact(Fact):
    action: Literal['confirm', 'cancel', 'settle', 'amend', 'delay', 'create_fact', 'irrelevant']
    new_amount: str | None
    new_currency: str | None
    new_date: date | None
    new_status: Status | None
    creates_new_event: bool
    # Additional nullable fact fields are necessary to safely materialize create_fact.
    event_description: str | None = None
    event_category: str | None = None
    event_direction: Direction | None = None
    event_type: str | None = None
    scope: Literal['single_occurrence', 'future_recurrence'] = 'single_occurrence'
    percentage_change: str | None = None

    _amount = field_validator('new_amount')(checked_amount)

    @field_validator('percentage_change')
    @classmethod
    def valid_percentage(cls, value: str | None) -> str | None:
        if value is not None:
            try:
                number = Decimal(value)
            except InvalidOperation:
                raise ValueError('invalid decimal percentage') from None
            if not number.is_finite() or number < -100:
                raise ValueError('percentage change must be finite and no smaller than -100')
        return value


class ExtractedFacts(BaseModel):
    model_config = ConfigDict(extra='forbid')
    images: list[ImageFact]
    messages: list[MessageFact]
