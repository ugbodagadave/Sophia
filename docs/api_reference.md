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

## Analysis
- rows_from_values(values: List[List[Any]], header: Optional[List[str]] = None) -> List[Dict[str, Any]]
- summarize_by_category(rows: Iterable[Dict[str, Any]], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Decimal]
- summarize_by_vendor(rows: Iterable[Dict[str, Any]], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Decimal]
- summarize_by_month(rows: Iterable[Dict[str, Any]], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Decimal]
- totals_and_averages(rows: Iterable[Dict[str, Any]], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]
- format_summary_for_slack(rows: Iterable[Dict[str, Any]], start_date: Optional[str] = None, end_date: Optional[str] = None) -> str
- classify_expense(vendor: str, description: str | None) -> str
- format_key_amount_map_for_slack(title: str, data: Dict[str, Decimal]) -> str
- format_overview_for_slack(total_formatted: str, average_formatted: str, count: int) -> str
- dicts_to_csv_string(rows: Iterable[Dict[str, object]], fieldnames: List[str]) -> str
- data_to_json_string(data: object) -> str

## Workflows
- process_slack_file_url(file_url: str) -> str
- handle_query(query: str) -> str
