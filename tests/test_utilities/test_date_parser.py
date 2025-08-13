from tools.utilities.date_parser import parse_date


def test_parse_date_iso():
	assert parse_date("2024-12-31") == "2024-12-31"


def test_parse_date_us():
	assert parse_date("12/31/2024") == "2024-12-31"


def test_parse_date_textual():
	assert parse_date("Dec 31, 2024") == "2024-12-31"


def test_parse_date_invalid():
	assert parse_date("31-31-9999") is None 