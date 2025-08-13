from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Optional, Tuple

from tools.utilities.currency_handler import normalize_amount, format_amount
from tools.utilities.date_parser import parse_date
from config.settings import get_settings


ExpenseRow = Dict[str, Any]


def _column_map() -> Dict[str, str]:
	# Map human column names to canonical lowercase keys
	# Uses data/templates/sheets_template.json ordering
	return {
		"Date": "date",
		"Vendor": "vendor",
		"Amount": "amount",
		"Category": "category",
		"Receipt_PDF_Link": "receipt_pdf_link",
		"Receipt_Image_Link": "receipt_image_link",
		"Description": "description",
		"Payment_Method": "payment_method",
		"Currency": "currency",
		"Confidence_Score": "confidence_score",
		"Processed_Date": "processed_date",
	}


def rows_from_values(values: List[List[Any]], header: Optional[List[str]] = None) -> List[ExpenseRow]:
	"""Convert sheet values (header + rows) into list of dicts keyed by template columns.
	If header is None, the first row in values is the header.
	"""
	if not values:
		return []
	if header is None:
		header = [str(h) for h in values[0]]
		data = values[1:]
	else:
		data = values
	mapping = _column_map()
	keyed_rows: List[ExpenseRow] = []
	for raw in data:
		row: ExpenseRow = {}
		for idx, col in enumerate(header):
			key = mapping.get(col, col)
			row[key] = raw[idx] if idx < len(raw) else None
		keyed_rows.append(row)
	return keyed_rows


def _in_date_range(row: ExpenseRow, start_date: Optional[str], end_date: Optional[str]) -> bool:
	if not start_date and not end_date:
		return True
	iso = row.get("date")
	if not iso:
		return False
	try:
		row_date = datetime.fromisoformat(str(iso)).date()
	except ValueError:
		parsed = parse_date(str(iso))
		if not parsed:
			return False
		row_date = datetime.fromisoformat(parsed).date()
	if start_date:
		if row_date < datetime.fromisoformat(start_date).date():
			return False
	if end_date:
		if row_date > datetime.fromisoformat(end_date).date():
			return False
	return True


def summarize_by_category(rows: Iterable[ExpenseRow], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Decimal]:
	buckets: Dict[str, Decimal] = defaultdict(Decimal)
	for row in rows:
		if not _in_date_range(row, start_date, end_date):
			continue
		amount = row.get("amount")
		amount_dec = None
		if isinstance(amount, (int, float, Decimal)):
			amount_dec = Decimal(str(amount))
		elif isinstance(amount, str):
			amount_dec = normalize_amount(amount)
		if amount_dec is None:
			continue
		category = str(row.get("category") or "Uncategorized")
		buckets[category] += amount_dec
	return dict(buckets)


def summarize_by_vendor(rows: Iterable[ExpenseRow], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Decimal]:
	buckets: Dict[str, Decimal] = defaultdict(Decimal)
	for row in rows:
		if not _in_date_range(row, start_date, end_date):
			continue
		amount = row.get("amount")
		amount_dec = None
		if isinstance(amount, (int, float, Decimal)):
			amount_dec = Decimal(str(amount))
		elif isinstance(amount, str):
			amount_dec = normalize_amount(amount)
		if amount_dec is None:
			continue
		vendor = str(row.get("vendor") or "Unknown")
		buckets[vendor] += amount_dec
	return dict(buckets)


def summarize_by_month(rows: Iterable[ExpenseRow], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Decimal]:
	buckets: Dict[str, Decimal] = defaultdict(Decimal)
	for row in rows:
		if not _in_date_range(row, start_date, end_date):
			continue
		amount = row.get("amount")
		if isinstance(amount, (int, float, Decimal)):
			amount_dec = Decimal(str(amount))
		elif isinstance(amount, str):
			amount_dec = normalize_amount(amount)
		else:
			amount_dec = None
		if amount_dec is None:
			continue
		date_val = row.get("date")
		parsed = None
		try:
			parsed = datetime.fromisoformat(str(date_val)).date()
		except Exception:
			parsed_text = parse_date(str(date_val)) if date_val else None
			if parsed_text:
				parsed = datetime.fromisoformat(parsed_text).date()
		if not parsed:
			continue
		key = f"{parsed.year:04d}-{parsed.month:02d}"
		buckets[key] += amount_dec
	return dict(buckets)


def totals_and_averages(rows: Iterable[ExpenseRow], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
	settings = get_settings()
	currency = settings.default_currency
	count = 0
	total = Decimal("0")
	for row in rows:
		if not _in_date_range(row, start_date, end_date):
			continue
		amount = row.get("amount")
		amount_dec = None
		if isinstance(amount, (int, float, Decimal)):
			amount_dec = Decimal(str(amount))
		elif isinstance(amount, str):
			amount_dec = normalize_amount(amount)
		if amount_dec is None:
			continue
		total += amount_dec
		count += 1
	average = (total / count) if count else Decimal("0")
	return {
		"count": count,
		"total": total,
		"average": average,
		"total_formatted": format_amount(total, currency),
		"average_formatted": format_amount(average, currency),
	}


def format_summary_for_slack(rows: Iterable[ExpenseRow], start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
	settings = get_settings()
	currency = settings.default_currency
	stats = totals_and_averages(list(rows), start_date, end_date)
	by_cat = summarize_by_category(list(rows), start_date, end_date)
	by_month = summarize_by_month(list(rows), start_date, end_date)
	# Sort for stable output
	cat_lines = [f"- {k}: {format_amount(v, currency)}" for k, v in sorted(by_cat.items())]
	month_lines = [f"- {k}: {format_amount(v, currency)}" for k, v in sorted(by_month.items())]
	parts = [
		"Expense Summary:",
		f"Total: {stats['total_formatted']} across {stats['count']} expenses",
		f"Average: {stats['average_formatted']}",
		"By Category:",
		*cat_lines,
		"By Month:",
		*month_lines,
	]
	return "\n".join(parts) 