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


def _mock_read(monkeypatch):
	from tools.data_management import sheets_reader as sr
	monkeypatch.setattr(sr, "read_range", lambda a1: VALUES)


def test_handle_query_summary(monkeypatch):
	__ = _mock_read(monkeypatch)
	text = handle_query("summary")
	assert "Expense Summary:" in text


def test_handle_query_by_category(monkeypatch):
	__ = _mock_read(monkeypatch)
	text = handle_query("by category")
	assert "Spend by Category:" in text


def test_handle_query_month_literal(monkeypatch):
	__ = _mock_read(monkeypatch)
	text = handle_query("summary for 2024-06")
	assert "Expense Summary:" in text


def test_handle_query_last_n_months(monkeypatch):
	__ = _mock_read(monkeypatch)
	text = handle_query("by month last 2 months")
	assert "Spend by Month:" in text


def test_handle_query_past_n_days(monkeypatch):
	__ = _mock_read(monkeypatch)
	text = handle_query("summary past 7 days")
	assert "Expense Summary:" in text


def test_handle_query_quarter(monkeypatch):
	__ = _mock_read(monkeypatch)
	text = handle_query("summary Q2 2024")
	assert "Expense Summary:" in text 