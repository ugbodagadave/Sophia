from __future__ import annotations

import csv
import io
import json
from decimal import Decimal
from typing import Dict, Iterable, List, Tuple

from config.settings import get_settings
from tools.utilities.currency_handler import format_amount


def format_key_amount_map_for_slack(title: str, data: Dict[str, Decimal]) -> str:
	settings = get_settings()
	currency = settings.default_currency
	lines = [title]
	for key in sorted(data.keys()):
		lines.append(f"- {key}: {format_amount(data[key], currency)}")
	return "\n".join(lines)


def format_overview_for_slack(total_formatted: str, average_formatted: str, count: int) -> str:
	return "\n".join([
		"Overview:",
		f"Total: {total_formatted} across {count} expenses",
		f"Average: {average_formatted}",
	])


def dicts_to_csv_string(rows: Iterable[Dict[str, object]], fieldnames: List[str]) -> str:
	buf = io.StringIO()
	writer = csv.DictWriter(buf, fieldnames=fieldnames)
	writer.writeheader()
	for row in rows:
		writer.writerow({k: row.get(k, "") for k in fieldnames})
	return buf.getvalue()


def data_to_json_string(data: object) -> str:
	return json.dumps(data, ensure_ascii=False, separators=(",", ":")) 