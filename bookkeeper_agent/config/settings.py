from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
	# IBM watsonx / Granite
	watsonx_api_key: Optional[str] = None
	watsonx_project_id: Optional[str] = None
	watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
	granite_model_id: str = "ibm/granite-3.3-8b-instruct"

	# Google
	google_sheets_credentials_path: str = "./config/google-credentials.json"
	google_sheets_spreadsheet_id: Optional[str] = None
	google_sheets_worksheet_name: str = "Expenses"
	google_drive_folder_id: Optional[str] = None

	# Slack
	slack_bot_token: Optional[str] = None
	slack_app_token: Optional[str] = None
	slack_signing_secret: Optional[str] = None
	slack_channel_id: Optional[str] = None

	# Storage
	file_storage_type: str = "google_drive"
	local_storage_path: str = "./data/file_storage/receipts/"
	cloud_storage_bucket: Optional[str] = None
	public_url_base: Optional[str] = None

	# OCR
	tesseract_cmd: Optional[str] = None
	tesseract_lang: str = "eng"
	ocr_confidence_threshold: int = 70
	image_preprocessing: bool = True

	# Processing
	max_file_size_mb: int = 10
	supported_image_formats: str = "jpg,jpeg,png,tiff,bmp"
	supported_pdf_max_pages: int = 5
	processing_timeout_seconds: int = 30

	# Logging
	log_level: str = "INFO"
	log_file_path: str = "./logs/bookkeeper.log"

	model_config = SettingsConfigDict(
		env_file=(
			Path(__file__).resolve().parent.parent / ".env",
			Path.cwd() / ".env",
		),
		env_file_encoding="utf-8",
		env_prefix="",
		case_sensitive=False,
	)

	@classmethod
	def from_environment(cls) -> "AppSettings":
		return cls(
			watsonx_api_key=None,
		)


def get_settings() -> AppSettings:
	return AppSettings() 