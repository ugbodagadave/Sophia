from __future__ import annotations

from typing import List, Any

from integrations.google_sheets import GoogleSheetsClient


def read_range(a1: str) -> List[List[Any]]:
	client = GoogleSheetsClient()
	return client.get_range(a1) 