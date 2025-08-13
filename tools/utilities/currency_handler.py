from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Optional


def normalize_amount(value: str) -> Optional[Decimal]:
	candidate = value.strip().replace(",", "").replace("$", "")
	try:
		return Decimal(candidate)
	except InvalidOperation:
		return None


def format_amount(amount: Decimal, currency: str = "USD") -> str:
	return f"{currency} {amount:.2f}" 