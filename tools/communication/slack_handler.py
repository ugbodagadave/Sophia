from __future__ import annotations

from pathlib import Path
from typing import Optional

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
	content = slack.download_file(file_url)

	# Determine type
	is_pdf = file_url.lower().endswith(".pdf")
	ext = None
	confidence = None

	storage = FileStorage()
	if is_pdf:
		filename = build_receipt_filename("unknown", vendor_hint or "vendor", amount_hint or "0", "pdf")
		stored = storage.save_bytes(f"pdf/{filename}", content)
		text = extract_pdf_text(stored)
	else:
		filename = build_receipt_filename("unknown", vendor_hint or "vendor", amount_hint or "0", "jpg")
		stored = storage.save_bytes(f"images/{filename}", content)
		pre = preprocess_image_for_ocr(stored)
		text, confidence = ocr_image_with_confidence(pre)

	parsed = parse_receipt_text(text or "")
	expense = {
		"Date": parsed.get("date"),
		"Vendor": parsed.get("vendor"),
		"Amount": parsed.get("amount"),
		"Category": parsed.get("category"),
		"Receipt_PDF_Link": storage.generate_public_link(f"pdf/{filename}") if is_pdf else "",
		"Receipt_Image_Link": storage.generate_public_link(f"images/{filename}") if not is_pdf else "",
	}
	try:
		append_expense_row(expense)
	except Exception:
		return format_error("Failed to write to Google Sheets. Check credentials and spreadsheet settings.")

	return format_receipt_summary(parsed, confidence) 