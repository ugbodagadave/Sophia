from pathlib import Path

import types

import tools.data_management.file_storage as fs_module
from tools.data_management.file_storage import FileStorage


class _StubSettings:
	def __init__(self, root: Path, public_base: str | None):
		self.file_storage_type = "local"
		self.local_storage_path = str(root)
		self.public_url_base = public_base


def test_save_bytes_and_public_link(tmp_path, monkeypatch):
	stub = _StubSettings(tmp_path, "http://localhost/receipts")
	monkeypatch.setattr(fs_module, "get_settings", lambda: stub)

	storage = FileStorage()
	out_path = storage.save_bytes("images/test.jpg", b"data")
	assert out_path.exists()

	link = storage.generate_public_link("images/test.jpg")
	assert link == "http://localhost/receipts/images/test.jpg"


def test_public_link_none_when_base_missing(tmp_path, monkeypatch):
	stub = _StubSettings(tmp_path, None)
	monkeypatch.setattr(fs_module, "get_settings", lambda: stub)

	storage = FileStorage()
	link = storage.generate_public_link("images/test.jpg")
	assert link is None 