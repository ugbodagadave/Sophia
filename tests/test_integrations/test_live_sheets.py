from __future__ import annotations

import os
import time
import pytest

from integrations.google_sheets import GoogleSheetsClient


@pytest.mark.live_sheets
def test_live_sheets_append_and_read_back():
	if os.getenv("RUN_LIVE") != "1" or os.getenv("RUN_LIVE_SHEETS") != "1":
		pytest.skip("RUN_LIVE and RUN_LIVE_SHEETS not set; skipping live Sheets test")

	client = GoogleSheetsClient()
	if client.service is None or not client.spreadsheet_id:
		pytest.skip("Google Sheets not configured; skipping")

	unique = f"live-test-{int(time.time())}"
	row = [unique, "Sophia", "1.23", "Test"]
	client.append_rows([row])

	values = client.get_range(f"{client.worksheet_name}!A1:Z")
	flat = ["|".join(r) for r in values]
	assert any(unique in x for x in flat) 