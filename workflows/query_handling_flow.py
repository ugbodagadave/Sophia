from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Tuple

from tools.data_management.sheets_reader import read_range
from tools.analysis.expense_analyzer import (
	rows_from_values,
	summarize_by_category,
	summarize_by_month,
	summarize_by_vendor,
	totals_and_averages,
	format_summary_for_slack,
)
from tools.analysis.report_generator import format_key_amount_map_for_slack


def _parse_simple_dates(query: str) -> tuple[str | None, str | None]:
	q = query.lower()
	today = date.today()
	if "last month" in q:
		first_this = date(today.year, today.month, 1)
		last_month_end = first_this - timedelta(days=1)
		last_month_start = date(last_month_end.year, last_month_end.month, 1)
		return last_month_start.isoformat(), last_month_end.isoformat()
	if "this month" in q:
		start = date(today.year, today.month, 1).isoformat()
		return start, today.isoformat()
	# yyyy-mm
	for token in q.split():
		if len(token) == 7 and token[4] == "-":
			try:
				y, m = token.split("-")
				start = date(int(y), int(m), 1)
				if m == "12":
					end = date(int(y) + 1, 1, 1) - timedelta(days=1)
				else:
					end = date(int(y), int(m) + 1, 1) - timedelta(days=1)
				return start.isoformat(), end.isoformat()
			except Exception:
				pass
	return None, None


def handle_query(query: str) -> str:
	"""Heuristic query handler for expense analytics.
	Supported:
	- summary
	- by category | by vendor | by month
	- top vendors N
	- largest expenses N
	- last month | this month | explicit yyyy-mm
	"""
	values: List[List[Any]] = read_range("Expenses!A:K")
	rows = rows_from_values(values)
	q = (query or "").lower()
	start, end = _parse_simple_dates(q)

	if "by category" in q:
		data = summarize_by_category(rows, start, end)
		return format_key_amount_map_for_slack("Spend by Category:", data)
	if "by vendor" in q:
		data = summarize_by_vendor(rows, start, end)
		return format_key_amount_map_for_slack("Spend by Vendor:", data)
	if "by month" in q:
		data = summarize_by_month(rows, start, end)
		return format_key_amount_map_for_slack("Spend by Month:", data)

	if "top vendors" in q:
		# extract N
		n = 5
		for tok in q.split():
			if tok.isdigit():
				n = int(tok)
				break
		data = summarize_by_vendor(rows, start, end)
		top = dict(sorted(data.items(), key=lambda kv: kv[1], reverse=True)[:n])
		return format_key_amount_map_for_slack("Top Vendors:", top)

	if "largest" in q and "expenses" in q:
		# build list of (vendor, amount, date)
		items = []
		for r in rows:
			if start or end:
				from tools.analysis.expense_analyzer import _in_date_range  # local import
				if not _in_date_range(r, start, end):
					continue
			amt = r.get("amount")
			try:
				val = Decimal(str(amt))
			except Exception:
				continue
			items.append((r.get("vendor") or "Unknown", val, r.get("date")))
		n = 5
		for tok in q.split():
			if tok.isdigit():
				n = int(tok)
				break
		items.sort(key=lambda x: x[1], reverse=True)
		lines = ["Largest Expenses:"]
		for vendor, amt, d in items[:n]:
			lines.append(f"- {d}: {vendor} {amt}")
		return "\n".join(lines)

	# default summary
	return format_summary_for_slack(rows, start, end) 