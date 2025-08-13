from __future__ import annotations

from pathlib import Path
from typing import Optional
from time import perf_counter

from integrations.slack_api import SlackClient
from tools.utilities.file_handler import build_receipt_filename
from tools.data_management.file_storage import FileStorage
from tools.document_processing.image_preprocessor import preprocess_image_for_ocr
from tools.document_processing.image_ocr import ocr_image_with_confidence
from tools.document_processing.pdf_extractor import extract_pdf_text
from tools.document_processing.receipt_parser import parse_receipt_text
from tools.data_management.sheets_writer import append_expense_row
from tools.communication.slack_formatter import format_receipt_summary, format_error, build_receipt_blocks


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
	if is_pdf:
		filename = build_receipt_filename("unknown", vendor_hint or "vendor", amount_hint or "0", "pdf")
		stored = storage.save_bytes(f"pdf/{filename}", content)
		text = extract_pdf_text(stored)
		pdf_link = storage.generate_public_link(f"pdf/{filename}")
		img_link = ""
	else:
		filename = build_receipt_filename("unknown", vendor_hint or "vendor", amount_hint or "0", "jpg")
		stored = storage.save_bytes(f"images/{filename}", content)
		pre = preprocess_image_for_ocr(stored)
		text, confidence = ocr_image_with_confidence(pre)
		pdf_link = ""
		img_link = storage.generate_public_link(f"images/{filename}")

	parsed = parse_receipt_text(text or "")
	expense = {
		"Date": parsed.get("date"),
		"Vendor": parsed.get("vendor"),
		"Amount": parsed.get("amount"),
		"Category": parsed.get("category"),
		"Receipt_PDF_Link": pdf_link,
		"Receipt_Image_Link": img_link,
	}
	try:
		append_expense_row(expense)
	except Exception:
		return format_error("Failed to write to Google Sheets. Check credentials and spreadsheet settings.")

	# Build Block Kit message
	processing_seconds = perf_counter() - start_time
	blocks = build_receipt_blocks(parsed, {"pdf": pdf_link, "image": img_link}, confidence, processing_seconds)
	# If configured, post to channel; otherwise return text for tests
	if slack.settings.slack_channel_id:
		slack.post_blocks(slack.settings.slack_channel_id, blocks, text="Receipt processed")

	return format_receipt_summary(parsed, confidence) 