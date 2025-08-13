import sys
import argparse
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from workflows.receipt_processing_flow import process_slack_file_url


def _read_file_bytes(p: Path) -> bytes:
	return p.read_bytes()


def main() -> None:
	parser = argparse.ArgumentParser(description="Sophia E2E Runner: process a Slack file URL end-to-end with optional mocks and verbose output.")
	parser.add_argument("file_url", help="Slack file URL to process (e.g., https://files.slack.com/...) or any URL ending with .pdf/.jpg/.png")
	parser.add_argument("--mock-download", dest="mock_download", default=None, help="Path to a local file to use instead of downloading from Slack")
	parser.add_argument("--real-sheets", dest="real_sheets", action="store_true", help="Actually write to Google Sheets (default is mock)")
	parser.add_argument("--real-slack-post", dest="real_slack_post", action="store_true", help="Actually send the Slack confirmation message (default is mock)")
	parser.add_argument("--show-ocr", dest="show_ocr", action="store_true", help="Print OCR/PDF text snippet and confidence if available")
	parser.add_argument("--show-parsed", dest="show_parsed", action="store_true", help="Print parsed fields merged from heuristics + Granite")
	parser.add_argument("--show-sheets-row", dest="show_sheets_row", action="store_true", help="Print the row dict that would be appended to Google Sheets")
	args = parser.parse_args()

	# Optional monkeypatches via runtime reassignment
	# 1. Slack download: optionally use a local file's bytes
	if args.mock_download:
		from integrations import slack_api as slack_mod
		local_path = Path(args.mock_download)
		if not local_path.exists():
			print(f"[e2e] mock download path not found: {local_path}")
			sys.exit(2)
		print(f"[e2e] Using mock download from local file: {local_path}")
		def _mock_download(self, url: str):
			return _read_file_bytes(local_path)
		slack_mod.SlackClient.download_file = _mock_download  # type: ignore

	# Observability holders
	observed: Dict[str, Any] = {"ocr": None, "ocr_conf": None, "pdf_text": None, "parsed": None, "sheets_row": None, "slack_msg": None}

	# 2. OCR and PDF extraction: wrap to capture outputs
	if args.show_ocr or args.show_parsed:
		from tools.document_processing import image_ocr as ocr_mod
		from tools.document_processing import pdf_extractor as pdf_mod
		from tools.document_processing import receipt_parser as rp_mod

		if hasattr(ocr_mod, "ocr_image_with_confidence"):
			_orig_ocr = ocr_mod.ocr_image_with_confidence
			def _wrap_ocr(image_path: Path) -> Tuple[str, Optional[float]]:
				text, conf = _orig_ocr(image_path)
				observed["ocr"], observed["ocr_conf"] = text, conf
				if args.show_ocr:
					preview = (text or "").strip().replace("\n", " ")[:300]
					print("[e2e] OCR text (first 300 chars):", preview)
					print("[e2e] OCR confidence:", conf)
				return text, conf
			ocr_mod.ocr_image_with_confidence = _wrap_ocr  # type: ignore

		if hasattr(pdf_mod, "extract_pdf_text"):
			_orig_pdf = pdf_mod.extract_pdf_text
			def _wrap_pdf(pdf_path: Path) -> str:
				text = _orig_pdf(pdf_path)
				observed["pdf_text"] = text
				if args.show_ocr:
					preview = (text or "").strip().replace("\n", " ")[:300]
					print("[e2e] PDF text (first 300 chars):", preview)
				return text
			pdf_mod.extract_pdf_text = _wrap_pdf  # type: ignore

		if args.show_parsed and hasattr(rp_mod, "parse_receipt_text"):
			_orig_parse = rp_mod.parse_receipt_text
			def _wrap_parse(t: str) -> Dict[str, Any]:
				data = _orig_parse(t)
				observed["parsed"] = data
				print("[e2e] Parsed fields:", data)
				return data
			rp_mod.parse_receipt_text = _wrap_parse  # type: ignore

	# 3. Sheets writer: wrap the symbol used by slack_handler to observe and optionally skip
	import tools.communication.slack_handler as sh
	_orig_append_from_sh = sh.append_expense_row
	def _wrap_append_from_sh(expense: Dict[str, Any]) -> None:
		observed["sheets_row"] = expense
		if args.show_sheets_row:
			print("[e2e] Google Sheets row:", expense)
		if args.real_sheets:
			return _orig_append_from_sh(expense)
		print("[e2e] Skipping real Google Sheets write (mock mode)")
	sh.append_expense_row = _wrap_append_from_sh  # type: ignore

	# Preflight connectivity for Sheets if requested
	if args.real_sheets:
		try:
			from integrations.google_sheets import GoogleSheetsClient
			client = GoogleSheetsClient()
			ok = bool(client.service and client.spreadsheet_id)
			print(f"[e2e] Google Sheets connectivity: {'OK' if ok else 'NOT CONFIGURED'} (service={'yes' if client.service else 'no'}, sheet_id={'set' if client.spreadsheet_id else 'unset'})")
		except Exception as exc:
			print("[e2e] Google Sheets connectivity check failed:", exc)

	# 4. Slack post_message: optionally mock and show message
	from integrations import slack_api as slack_mod
	_orig_post = slack_mod.SlackClient.post_message
	def _wrap_post(self, channel: str, text: str) -> Optional[str]:
		observed["slack_msg"] = text
		print("[e2e] Slack confirmation text:", text)
		if args.real_slack_post:
			return _orig_post(self, channel, text)
		print("[e2e] Skipping real Slack post (mock mode)")
		return None
	slack_mod.SlackClient.post_message = _wrap_post  # type: ignore

	# Execute the full flow
	print(f"[e2e] Processing URL: {args.file_url}")
	result = process_slack_file_url(args.file_url)
	print("\n--- User-visible result ---")
	print(result)
	print("---------------------------")


if __name__ == "__main__":
	main() 