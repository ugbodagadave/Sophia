from __future__ import annotations

from pathlib import Path
from typing import Optional

from config.settings import get_settings
from tools.utilities.file_handler import ensure_directory, write_bytes
from integrations.google_drive import GoogleDriveClient


class FileStorage:
	def __init__(self) -> None:
		self.settings = get_settings()
		self.storage_type = self.settings.file_storage_type
		self.local_root = Path(self.settings.local_storage_path)

	def save_bytes(self, relative_path: str, data: bytes) -> str | Path:
		if self.storage_type == "local":
			destination = self.local_root / relative_path
			ensure_directory(destination.parent)
			return write_bytes(destination, data)
		if self.storage_type == "google_drive":
			client = GoogleDriveClient()
			folder_id = self.settings.google_drive_folder_id
			if not folder_id:
				raise ValueError("google_drive_folder_id must be set in .env for Google Drive storage")
			file_name = Path(relative_path).name
			content_type = "image/jpeg" if file_name.endswith(".jpg") else "application/pdf"
			link = client.upload_file(file_name, data, content_type, folder_id)
			return link or ""
		raise NotImplementedError(f"Storage type not implemented: {self.storage_type}")

	def generate_public_link(self, stored_path: str | Path) -> Optional[str]:
		if self.storage_type == "local":
			if not self.settings.public_url_base:
				return None
			return f"{self.settings.public_url_base.rstrip('/')}/{str(stored_path).replace('\\', '/')}"
		if self.storage_type == "google_drive":
			return str(stored_path)  # The path returned from save_bytes is already the public link
		raise NotImplementedError(f"Storage type not implemented: {self.storage_type}") 