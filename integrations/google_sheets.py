from __future__ import annotations

from typing import List, Dict, Any

from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import get_settings


SCOPES = [
	"https://www.googleapis.com/auth/spreadsheets",
	"https://www.googleapis.com/auth/drive.readonly",
]


class GoogleSheetsClient:
	def __init__(self) -> None:
		# Lazy import to prevent module import-time dependency failures
		from google.oauth2.service_account import Credentials
		from googleapiclient.discovery import build

		self.settings = get_settings()
		creds = Credentials.from_service_account_file(
			self.settings.google_sheets_credentials_path,
			scopes=SCOPES,
		)
		self.service = build("sheets", "v4", credentials=creds)
		self.spreadsheet_id = self.settings.google_sheets_spreadsheet_id
		self.worksheet_name = self.settings.google_sheets_worksheet_name

	@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=1, max=4))
	def append_rows(self, rows: List[List[Any]]) -> Dict[str, Any]:
		range_name = f"{self.worksheet_name}!A1"
		body = {"values": rows}
		return (
			self.service.spreadsheets()
			.values()
			.append(spreadsheetId=self.spreadsheet_id, range=range_name, valueInputOption="USER_ENTERED", body=body)
			.execute()
		)

	@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=1, max=4))
	def get_range(self, range_a1: str) -> List[List[Any]]:
		result = (
			self.service.spreadsheets()
			.values()
			.get(spreadsheetId=self.spreadsheet_id, range=range_a1)
			.execute()
		)
		return result.get("values", []) 