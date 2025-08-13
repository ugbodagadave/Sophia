# API Reference

## Integrations
- GoogleSheetsClient
  - append_rows(rows: List[List[Any]]) -> Dict[str, Any]
  - get_range(range_a1: str) -> List[List[Any]]
- SlackClient
  - post_message(channel: str, text: str) -> Optional[str]
  - download_file(url: str) -> bytes

## Document Processing
- extract_pdf_text(pdf_path: Path) -> str
- preprocess_image_for_ocr(image_path: Path, threshold: bool = False) -> Path
- ocr_image_to_text(image_path: Path) -> str
- ocr_image_with_confidence(image_path: Path) -> Tuple[str, Optional[float]]
- parse_receipt_text(text: str) -> Dict[str, Any]

## Data Management
- FileStorage
  - save_bytes(relative_path: str, data: bytes) -> Path
  - generate_public_link(relative_path: str) -> Optional[str]
- append_expense_row(expense: Dict[str, Any]) -> None
- read_range(a1: str) -> List[List[Any]]

## Communication
- format_receipt_summary(parsed: Dict[str, Any], confidence: float | None = None) -> str
- format_error(message: str) -> str
- handle_slack_file(file_url: str, vendor_hint: Optional[str] = None, amount_hint: Optional[str] = None) -> str
- send_status(text: str) -> None

## Workflows
- process_slack_file_url(file_url: str) -> str
