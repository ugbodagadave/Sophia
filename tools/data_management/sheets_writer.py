from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List

from integrations.google_sheets import GoogleSheetsClient


def _load_columns() -> List[str]:
	template_path = Path("data/templates/sheets_template.json")
	columns = json.loads(template_path.read_text(encoding="utf-8")).get("columns", [])
	return columns


def append_expense_row(expense: Dict[str, Any]) -> None:
	columns = _load_columns()
	row = [expense.get(col, "") for col in columns]
	client = GoogleSheetsClient()
	client.append_rows([row]) 