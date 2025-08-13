from __future__ import annotations

from workflows.query_handling_flow import handle_query

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


def test_handle_query_summary(monkeypatch):
	from tools.data_management import sheets_reader as sr
	monkeypatch.setattr(sr, "read_range", lambda a1: VALUES)
	text = handle_query("summary")
	assert "Expense Summary:" in text


def test_handle_query_by_category(monkeypatch):
	from tools.data_management import sheets_reader as sr
	monkeypatch.setattr(sr, "read_range", lambda a1: VALUES)
	text = handle_query("by category")
	assert "Spend by Category:" in text


def test_handle_query_last_month(monkeypatch):
	from tools.data_management import sheets_reader as sr
	monkeypatch.setattr(sr, "read_range", lambda a1: VALUES)
	text = handle_query("summary for 2024-06")
	assert "Expense Summary:" in text 