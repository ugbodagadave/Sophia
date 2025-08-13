from __future__ import annotations

from tools.communication.slack_handler import handle_slack_file


def test_e2e_receipt_processing_monkeypatched(monkeypatch, tmp_path):
	# Patch Slack download to return fake JPG bytes
	from integrations import slack_api as slack_mod
	monkeypatch.setattr(slack_mod.SlackClient, "download_file", lambda self, url: b"fake-bytes")
	# Patch file storage save to write bytes to tmp and return path
	from tools.data_management import file_storage as fs_mod
	def fake_save(self, rel, data: bytes):
		p = tmp_path / rel.replace("/", "_")
		p.parent.mkdir(parents=True, exist_ok=True)
		p.write_bytes(data)
		return p
	monkeypatch.setattr(fs_mod.FileStorage, "save_bytes", fake_save)
	monkeypatch.setattr(fs_mod.FileStorage, "generate_public_link", lambda self, rel: f"https://example.com/{rel}")
	# Patch preprocessing and OCR directly on slack_handler symbols
	import tools.communication.slack_handler as sh
	monkeypatch.setattr(sh, "preprocess_image_for_ocr", lambda path: path)
	text = """
	ACME STORE
	Date: 12/31/2024
	Total: 15.99
	"""
	monkeypatch.setattr(sh, "ocr_image_with_confidence", lambda p: (text, 94.0))
	# Capture appended row by patching slack_handler.append_expense_row
	captured = {}
	monkeypatch.setattr(sh, "append_expense_row", lambda expense: captured.update(expense))
	# Execute
	summary = handle_slack_file("https://files.slack.com/fake.jpg")
	assert summary == "Receipt added to Google Sheet."
	# Ensure row would have been sent
	assert captured.get("Vendor") == "ACME STORE" 