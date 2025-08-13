from tools.document_processing.receipt_parser import heuristic_parse


def test_heuristic_parse_vendor_and_date_and_amount():
	text = """
	ACME STORE
	Date: 12/31/2024
	Total: 15.99
	"""
	parsed = heuristic_parse(text)
	assert parsed["vendor"] == "ACME STORE"
	assert parsed["date"] == "2024-12-31"
	assert parsed["amount"] == 15.99


def test_heuristic_parse_missing_amount():
	text = """
	My Shop
	2024-01-05
	Thank you
	"""
	parsed = heuristic_parse(text)
	assert parsed["vendor"] == "My Shop"
	assert parsed["date"] == "2024-01-05"
	assert parsed["amount"] is None 