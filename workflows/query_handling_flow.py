from __future__ import annotations

from typing import Any, Dict, List, Tuple

from tools.data_management.sheets_reader import read_range
from tools.analysis.expense_analyzer import rows_from_values, summarize_by_category, summarize_by_month, summarize_by_vendor, totals_and_averages, format_summary_for_slack


def handle_query(query: str) -> str:
	"""Very simple heuristic query handler.
	Supported intents: summary, by category, by vendor, by month.
	Reads entire worksheet range A:K (per template) assuming header row present.
	"""
	values: List[List[Any]] = read_range("Expenses!A:K")
	rows = rows_from_values(values)
	q = (query or "").lower()
	if "by category" in q:
		data = summarize_by_category(rows)
		lines = ["Spend by Category:"] + [f"- {k}: {v}" for k, v in sorted(data.items())]
		return "\n".join(lines)
	if "by vendor" in q:
		data = summarize_by_vendor(rows)
		lines = ["Spend by Vendor:"] + [f"- {k}: {v}" for k, v in sorted(data.items())]
		return "\n".join(lines)
	if "by month" in q:
		data = summarize_by_month(rows)
		lines = ["Spend by Month:"] + [f"- {k}: {v}" for k, v in sorted(data.items())]
		return "\n".join(lines)
	# default summary
	return format_summary_for_slack(rows) 