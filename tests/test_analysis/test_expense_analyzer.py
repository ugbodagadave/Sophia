from __future__ import annotations

from decimal import Decimal

from tools.analysis.expense_analyzer import rows_from_values, summarize_by_category, summarize_by_vendor, summarize_by_month, totals_and_averages, format_summary_for_slack


HEADER = [
	"Date",
	"Vendor",
	"Amount",
	"Category",
	"Receipt_PDF_Link",
	"Receipt_Image_Link",
	"Description",
	"Payment_Method",
	"Currency",
	"Confidence_Score",
	"Processed_Date",
]

VALUES = [
	HEADER,
	["2024-06-01", "Starbucks", "5.50", "Dining", "", "", "Coffee", "Card", "USD", "95", "2024-06-01"],
	["2024-06-15", "Uber", "12.00", "Transport", "", "", "Ride", "Card", "USD", "", "2024-06-15"],
	["2024-07-03", "Walmart", "30.25", "Groceries", "", "", "Snacks", "Card", "USD", "", "2024-07-03"],
]


def test_rows_from_values_maps_columns():
	rows = rows_from_values(VALUES)
	assert rows[0]["vendor"] == "Starbucks"
	assert rows[1]["category"] == "Transport"


def test_summaries():
	rows = rows_from_values(VALUES)
	by_cat = summarize_by_category(rows)
	assert by_cat["Dining"] == Decimal("5.50")
	assert by_cat["Transport"] == Decimal("12.00")
	by_vendor = summarize_by_vendor(rows)
	assert by_vendor["Starbucks"] == Decimal("5.50")
	by_month = summarize_by_month(rows)
	assert by_month["2024-06"] == Decimal("17.50")
	stats = totals_and_averages(rows)
	assert stats["count"] == 3
	assert stats["total"] == Decimal("47.75")


def test_format_summary_for_slack_contains_sections():
	rows = rows_from_values(VALUES)
	text = format_summary_for_slack(rows)
	assert "Expense Summary:" in text
	assert "By Category:" in text
	assert "By Month:" in text 