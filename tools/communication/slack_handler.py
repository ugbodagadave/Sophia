from __future__ import annotations

from pathlib import Path
from typing import Optional
from time import perf_counter
import tempfile

from integrations.slack_api import SlackClient
from tools.utilities.file_handler import build_receipt_filename
from tools.data_management.file_storage import FileStorage
from tools.document_processing.image_preprocessor import preprocess_image_for_ocr
from tools.document_processing.image_ocr import ocr_image_with_confidence
from tools.document_processing.pdf_extractor import extract_pdf_text
from tools.document_processing.receipt_parser import parse_receipt_text
from tools.data_management.sheets_writer import append_expense_row
from tools.communication.slack_formatter import format_receipt_summary, format_error


def handle_slack_file(file_url: str, vendor_hint: Optional[str] = None, amount_hint: Optional[str] = None) -> str:
	# Download file
	slack = SlackClient()
	start_time = perf_counter()
	response = slack.download_file(file_url)
	# Support both requests.Response and raw bytes (for tests/monkeypatches)
	if isinstance(response, (bytes, bytearray)):
		content = bytes(response)
		content_type = ""
	else:
		content = response.content  # type: ignore[attr-defined]
		content_type = getattr(response, "headers", {}).get("Content-Type", "").lower()  # type: ignore[attr-defined]

	# Determine type from Content-Type header or URL
	is_pdf = "pdf" in content_type or file_url.lower().endswith(".pdf")
	confidence = None

	storage = FileStorage()
	reference_link: Optional[str] = None
	# Create a temp file to run local processing regardless of storage backend
	with tempfile.TemporaryDirectory() as tmpdir:
		if is_pdf:
			filename = build_receipt_filename("unknown", vendor_hint or "vendor", amount_hint or "0", "pdf")
			tmp_path = Path(tmpdir) / filename
			tmp_path.write_bytes(content)
			text = extract_pdf_text(tmp_path)
			# After local processing, upload original bytes to storage and build link
			stored = storage.save_bytes(f"pdf/{filename}", content)
			reference_link = storage.generate_public_link(f"pdf/{filename}")
		else:
			filename = build_receipt_filename("unknown", vendor_hint or "vendor", amount_hint or "0", "jpg")
			tmp_path = Path(tmpdir) / filename
			tmp_path.write_bytes(content)
			pre = preprocess_image_for_ocr(tmp_path)
			text, confidence = ocr_image_with_confidence(pre)
			# After local processing, upload original bytes to storage and build link
			stored = storage.save_bytes(f"images/{filename}", content)
			reference_link = storage.generate_public_link(f"images/{filename}")

	parsed = parse_receipt_text(text or "")
	expense = {
		"Date": parsed.get("date"),
		"Vendor": parsed.get("vendor"),
		"Amount": parsed.get("amount"),
		"Category": parsed.get("category"),
		"Receipt_PDF_Link": reference_link if is_pdf else "",
		"Receipt_Image_Link": reference_link if not is_pdf else "",
		"Reference": reference_link or "",
	}
	try:
		append_expense_row(expense)
	except Exception:
		return format_error("Failed to write to Google Sheets. Check credentials and spreadsheet settings.")

	# Only confirmation message to the user
	if slack.settings.slack_channel_id:
		slack.post_message(slack.settings.slack_channel_id, text=format_receipt_summary(parsed, confidence))

	return format_receipt_summary(parsed, confidence) 