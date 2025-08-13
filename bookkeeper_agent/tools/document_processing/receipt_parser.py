from __future__ import annotations

import re
from decimal import Decimal
from typing import Dict, Any

from bookkeeper_agent.models.granite_client import GraniteClient
from bookkeeper_agent.tools.utilities.date_parser import parse_date
from bookkeeper_agent.tools.utilities.currency_handler import normalize_amount


DATE_REGEXES = [
	r"(\d{4}-\d{2}-\d{2})",
	r"(\d{2}/\d{2}/\d{4})",
	r"(\d{2}/\d{2}/\d{2,4})",
]
AMOUNT_REGEX = r"(?:total|amount|sum)\D{0,5}(\d+[\.,]?\d{0,2})"


def heuristic_parse(text: str) -> Dict[str, Any]:
	result: Dict[str, Any] = {"date": None, "vendor": None, "amount": None, "category": None}
	lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
	if lines:
		result["vendor"] = lines[0][:80]
	# date
	for rx in DATE_REGEXES:
		m = re.search(rx, text, re.IGNORECASE)
		if m:
			iso = parse_date(m.group(1))
			if iso:
				result["date"] = iso
				break
	# amount
	m2 = re.search(AMOUNT_REGEX, text, re.IGNORECASE)
	if m2:
		amt = m2.group(1).replace(",", "")
		try:
			result["amount"] = float(Decimal(amt))
		except Exception:
			pass
	return result


def parse_receipt_text(text: str) -> Dict[str, Any]:
	data = heuristic_parse(text)
	client = GraniteClient()
	try:
		granite_data = client.extract_receipt_data(text)
		data.update({k: v for k, v in granite_data.items() if v})
	except Exception:
		pass
	return data 