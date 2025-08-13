from __future__ import annotations

from decimal import Decimal

from tools.analysis.report_generator import format_key_amount_map_for_slack, format_overview_for_slack, dicts_to_csv_string, data_to_json_string


def test_format_key_amount_map_for_slack():
	text = format_key_amount_map_for_slack("By Category:", {"Dining": Decimal("10.00"), "Groceries": Decimal("5.00")})
	assert text.startswith("By Category:")
	assert "Dining" in text and "Groceries" in text


def test_format_overview_for_slack():
	text = format_overview_for_slack("USD 15.00", "USD 7.50", 2)
	assert "Total: USD 15.00 across 2 expenses" in text
	assert "Average: USD 7.50" in text


def test_csv_and_json_outputs():
	rows = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
	csv_str = dicts_to_csv_string(rows, ["a", "b"])
	assert csv_str.splitlines()[0] == "a,b"
	json_str = data_to_json_string({"x": 1})
	assert json_str == "{\"x\":1}" 