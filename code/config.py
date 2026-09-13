"""Configuration never grants permission to make live calls."""
import os
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / '.env')


def model_name() -> str:
    return os.environ.get('OPENAI_EVIDENCE_MODEL', os.environ.get('OPENAI_MODEL', 'gpt-4.1-mini'))


def token_rate(name: str) -> Decimal | None:
    value = os.environ.get(name)
    if not value:
        return None
    rate = Decimal(value)
    if not rate.is_finite() or rate < 0:
        raise ValueError(f'{name} must be a nonnegative decimal')
    return rate
