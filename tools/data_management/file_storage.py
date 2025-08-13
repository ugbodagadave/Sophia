from __future__ import annotations

from pathlib import Path
from typing import Optional
import mimetypes

from config.settings import get_settings
from tools.utilities.file_handler import ensure_directory, write_bytes
from integrations.postgres_storage import PostgresStorageClient


class FileStorage:
	def __init__(self) -> None:
		self.settings = get_settings()
		self.storage_type = self.settings.file_storage_type
		self.local_root = Path(self.settings.local_storage_path)

	def _guess_mime(self, relative_path: str) -> str:
		mime, _ = mimetypes.guess_type(relative_path)
		return mime or "application/octet-stream"

	def save_bytes(self, relative_path: str, data: bytes) -> str | Path:
		if self.storage_type == "local":
			destination = self.local_root / relative_path
			ensure_directory(destination.parent)
			return write_bytes(destination, data)
		if self.storage_type == "postgres":
			client = PostgresStorageClient()
			content_type = self._guess_mime(relative_path)
			file_id = client.save_bytes(relative_path, data, content_type)
			return file_id
		raise NotImplementedError(f"Storage type not implemented: {self.storage_type}")

	def generate_public_link(self, stored_path: str | Path) -> Optional[str]:
		if self.storage_type == "local":
			if not self.settings.public_url_base:
				return None
			return f"{self.settings.public_url_base.rstrip('/')}/{str(stored_path).replace('\\', '/')}"
		if self.storage_type == "postgres":
			client = PostgresStorageClient()
			return client.build_public_link(str(stored_path))
		raise NotImplementedError(f"Storage type not implemented: {self.storage_type}") 