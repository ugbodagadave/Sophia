from __future__ import annotations

from io import BytesIO

from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import get_settings

try:
	from google.oauth2.service_account import Credentials
	from googleapiclient.discovery import build
	from googleapiclient.http import MediaIoBaseUpload
except ImportError:
	Credentials = None
	build = None
	MediaIoBaseUpload = None


SCOPES = [
	"https://www.googleapis.com/auth/drive",
]


class GoogleDriveClient:
	def __init__(self) -> None:
		self.settings = get_settings()
		if Credentials is None or build is None:
			self.service = None
		else:
			creds = Credentials.from_service_account_file(
				self.settings.google_sheets_credentials_path, scopes=SCOPES
			)
			self.service = build("drive", "v3", credentials=creds)

	@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=1, max=4))
	def upload_file(self, file_name: str, file_content: bytes, content_type: str, folder_id: str) -> str | None:
		if not self.service or MediaIoBaseUpload is None:
			return None
		file_metadata = {"name": file_name, "parents": [folder_id]}
		media = MediaIoBaseUpload(BytesIO(file_content), mimetype=content_type, resumable=True)
		file = self.service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
		return file.get("webViewLink") 