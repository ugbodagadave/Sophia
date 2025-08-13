from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Tuple
import re

from tools.data_management.sheets_reader import read_range
from tools.analysis.expense_analyzer import (
	rows_from_values,
	summarize_by_category,
	summarize_by_month,
	summarize_by_vendor,
	totals_and_averages,
	format_summary_for_slack,
)
from tools.analysis.report_generator import format_key_amount_map_for_slack, save_report_csv, save_report_json, build_fields_with_percentages
from integrations.slack_api import SlackClient
from tools.communication.slack_formatter import build_analytics_blocks


def _parse_simple_dates(query: str) -> tuple[str | None, str | None]:
	q = query.lower()
	today = date.today()
	# last N months
	m_last = re.search(r"last\s+(\d+)\s+months?", q)
	if m_last:
		n = max(1, int(m_last.group(1)))
		first_this = date(today.year, today.month, 1)
		end = today
		# compute start by going back n-1 months from first day of this month
		y, m = first_this.year, first_this.month
		for _ in range(n):
			m -= 1
			if m == 0:
				y -= 1
				m = 12
		start = date(y, m, 1)
		return start.isoformat(), end.isoformat()
	# past N days
	m_days = re.search(r"past\s+(\d+)\s+days?", q)
	if m_days:
		n = max(1, int(m_days.group(1)))
		start = today - timedelta(days=n)
		return start.isoformat(), today.isoformat()
	# quarters: q[1-4] yyyy or q[1-4]-yyyy
	m_q = re.search(r"q([1-4])[-\s]?([12][0-9]{3})", q)
	if m_q:
		qnum = int(m_q.group(1))
		year = int(m_q.group(2))
		start_month = (qnum - 1) * 3 + 1
		start = date(year, start_month, 1)
		if start_month == 10:
			end = date(year + 1, 1, 1) - timedelta(days=1)
		else:
			end = date(year, start_month + 3, 1) - timedelta(days=1)
		return start.isoformat(), end.isoformat()
	if "last month" in q:
		first_this = date(today.year, today.month, 1)
		last_month_end = first_this - timedelta(days=1)
		last_month_start = date(last_month_end.year, last_month_end.month, 1)
		return last_month_start.isoformat(), last_month_end.isoformat()
	if "this month" in q:
		start = date(today.year, today.month, 1).isoformat()
		return start, today.isoformat()
	# yyyy-mm explicit month
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
	- last month | this month | explicit yyyy-mm | last N months | past N days | Q[1-4] YYYY
	- export csv/json (append 'export csv' or 'export json')
	"""
	values: List[List[Any]] = read_range("Expenses!A:K")
	rows = rows_from_values(values)
	q = (query or "").lower()
	start, end = _parse_simple_dates(q)

	export_csv = "export csv" in q
	export_json = "export json" in q

	if "by category" in q:
		data = summarize_by_category(rows, start, end)
		if export_csv:
			link = save_report_csv("reports/by_category.csv", [{"Category": k, "Amount": str(v)} for k, v in data.items()], ["Category", "Amount"])
			return f"Report saved: {link}" if link else format_key_amount_map_for_slack("Spend by Category:", data)
		if export_json:
			link = save_report_json("reports/by_category.json", {k: str(v) for k, v in data.items()})
			return f"Report saved: {link}" if link else format_key_amount_map_for_slack("Spend by Category:", data)
		# Also attempt Block Kit if configured
		settings_client = SlackClient()
		if settings_client.settings.slack_channel_id:
			fields = build_fields_with_percentages(data)
			blocks = build_analytics_blocks("📊 Spend by Category", "Totals by category", fields)
			settings_client.post_blocks(settings_client.settings.slack_channel_id, blocks, text="Analytics")
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
		from tools.analysis.expense_analyzer import _in_date_range  # local import
		for r in rows:
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