from tools.communication.slack_formatter import format_receipt_summary, format_error


def test_format_receipt_summary_basic():
	msg = format_receipt_summary({"date": "2024-12-31", "vendor": "Store", "amount": 12.34, "category": "Food"})
	assert "Receipt processed:" in msg
	assert "Date: 2024-12-31" in msg
	assert "Vendor: Store" in msg
	assert "Amount: 12.34" in msg
	assert "Category: Food" in msg


def test_format_receipt_summary_with_conf():
	msg = format_receipt_summary({"date": None, "vendor": None, "amount": None, "category": None}, 88.5)
	assert "OCR Confidence: 88.5%" in msg


def test_format_error():
	assert ":warning:" in format_error("Oops") 