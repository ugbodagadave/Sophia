from __future__ import annotations

import os
import pytest

from workflows.receipt_processing_flow import process_slack_file_url
from integrations.google_sheets import GoogleSheetsClient


@pytest.mark.live_e2e
def test_live_e2e_process_slack_file_url():
	if os.getenv("RUN_LIVE") != "1" or os.getenv("RUN_LIVE_E2E") != "1":
		pytest.skip("RUN_LIVE and RUN_LIVE_E2E not set; skipping live E2E test")

	file_url = os.getenv("E2E_FILE_URL")
	if not file_url:
		pytest.skip("E2E_FILE_URL not provided; skipping")

	msg = process_slack_file_url(file_url)
	assert msg == "Receipt added to Google Sheet."

	if os.getenv("RUN_LIVE_SHEETS_VERIFY") == "1":
		client = GoogleSheetsClient()
		if client.service and client.spreadsheet_id:
			values = client.get_range(f"{client.worksheet_name}!A1:Z")
			assert isinstance(values, list) 