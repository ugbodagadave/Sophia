import json
from pathlib import Path

import types
import sys

from tools.data_management import sheets_writer


def test_append_expense_row_monkeypatch(tmp_path, monkeypatch):
	# Prepare a temporary template file
	template_dir = tmp_path / "data" / "templates"
	template_dir.mkdir(parents=True)
	template = template_dir / "sheets_template.json"
	template.write_text(json.dumps({"columns": ["Date", "Vendor", "Amount", "Category"]}), encoding="utf-8")

	# Monkeypatch function to load columns to use the temp template
	monkeypatch.setattr(sheets_writer, "_load_columns", lambda: ["Date", "Vendor", "Amount", "Category"]) 

	# Stub GoogleSheetsClient
	calls = {"rows": None}
	class StubClient:
		def append_rows(self, rows):
			calls["rows"] = rows
			return {"updates": {"updatedRows": len(rows)}}

	monkeypatch.setattr(sheets_writer, "GoogleSheetsClient", StubClient)

	expense = {"Date": "2024-12-31", "Vendor": "Store", "Amount": 10.5, "Category": "Food"}
	sheets_writer.append_expense_row(expense)

	assert calls["rows"] == [["2024-12-31", "Store", 10.5, "Food"]] 