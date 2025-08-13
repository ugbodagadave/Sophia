from __future__ import annotations

from pathlib import Path
from typing import Optional

from config.settings import get_settings
from tools.utilities.file_handler import ensure_directory, write_bytes


class FileStorage:
	def __init__(self) -> None:
		self.settings = get_settings()
		self.storage_type = self.settings.file_storage_type
		self.local_root = Path(self.settings.local_storage_path)

	def save_bytes(self, relative_path: str, data: bytes) -> Path:
		if self.storage_type == "local":
			destination = self.local_root / relative_path
			ensure_directory(destination.parent)
			return write_bytes(destination, data)
		raise NotImplementedError(f"Storage type not implemented: {self.storage_type}")

	def generate_public_link(self, relative_path: str) -> Optional[str]:
		if self.storage_type == "local":
			if not self.settings.public_url_base:
				return None
			return f"{self.settings.public_url_base.rstrip('/')}/{relative_path.replace('\\', '/')}"
		raise NotImplementedError(f"Storage type not implemented: {self.storage_type}") 