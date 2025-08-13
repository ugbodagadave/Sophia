# API Reference

## Integrations
- GoogleSheetsClient
  - append_rows(rows: List[List[Any]]) -> Dict[str, Any]
  - get_range(range_a1: str) -> List[List[Any]]
- SlackClient
  - post_message(channel: str, text: str) -> Optional[str]
  - post_blocks(channel: str, blocks: List[Dict[str, Any]], text: str = "") -> Optional[str]
  - download_file(url: str) -> bytes|Response

## Document Processing
- extract_pdf_text(pdf_path: Path) -> str
- preprocess_image_for_ocr(image_path: Path, threshold: bool = False) -> Path
- ocr_image_to_text(image_path: Path) -> str
- ocr_image_with_confidence(image_path: Path) -> Tuple[str, Optional[float]]
- parse_receipt_text(text: str) -> Dict[str, Any]

## Data Management
- FileStorage (local or postgres)
  - save_bytes(relative_path: str, data: bytes) -> Path|str
  - generate_public_link(relative_path: str) -> Optional[str]
- append_expense_row(expense: Dict[str, Any]) -> None
- read_range(a1: str) -> List[List[Any]]

## Communication
- format_receipt_summary(parsed: Dict[str, Any], confidence: float | None = None) -> str
- format_error(message: str) -> str

## Models
- GraniteClient
  - extract_receipt_data(text: str) -> Dict[str, Any]
    - Retries (up to 3 attempts) with exponential backoff
    - Parses first JSON object from model output
    - Validates/coerces via schema: date (ISO), vendor (str), amount (float), category (str)
    - On errors, logs structured warning and returns {}
  - suggest_category(vendor: str, description: Optional[str] = None) -> str
    - Retries (up to 3 attempts) with exponential backoff
    - Returns short category string; defaults to "Uncategorized" on failure

## Workflows
- process_slack_file_url(file_url: str) -> str
- handle_query(query: str) -> str
  - Supports date ranges and optional exports

Notes
- The Google Sheet now includes a last column `Reference` which contains a single link to the stored receipt (image or PDF).
- Slack replies only confirm success and do not include links or interactive buttons.

## Live Tests

Sophia includes comprehensive live integration tests that verify functionality against real services. These tests are **disabled by default** and require specific environment variables to be set.

### Environment Variables Required

**Global Live Test Flag:**
```
RUN_LIVE=1
```

**Slack Live Tests:**
```
RUN_LIVE_SLACK=1
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_CHANNEL_ID=C1234567890
```

**Google Sheets Live Tests:**
```
RUN_LIVE_SHEETS=1
GOOGLE_SHEETS_CREDENTIALS_PATH=./config/google-credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_SHEETS_WORKSHEET_NAME=Expenses
```

**OCR Live Tests:**
```
RUN_LIVE_OCR=1
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
TESSERACT_LANG=eng
```

**End-to-End Live Tests:**
```
RUN_LIVE_E2E=1
E2E_FILE_URL=https://files.slack.com/files-pri/T1234567890-F1234567890/download/receipt.jpg
# Optional verification
RUN_LIVE_SHEETS_VERIFY=1
```

### Running Live Tests

**Windows (PowerShell):**
```powershell
# Slack tests
$env:RUN_LIVE="1"; $env:RUN_LIVE_SLACK="1"; pytest -m live_slack -q

# Google Sheets tests
$env:RUN_LIVE="1"; $env:RUN_LIVE_SHEETS="1"; pytest -m live_sheets -q

# OCR tests
$env:RUN_LIVE="1"; $env:RUN_LIVE_OCR="1"; pytest -m live_ocr -q

# End-to-end tests
$env:RUN_LIVE="1"; $env:RUN_LIVE_E2E="1"; $env:E2E_FILE_URL="https://files.slack.com/..."; pytest -m live_e2e -q
```

**Windows (Command Prompt):**
```cmd
# Slack tests
set RUN_LIVE=1 && set RUN_LIVE_SLACK=1 && pytest -m live_slack -q

# Google Sheets tests
set RUN_LIVE=1 && set RUN_LIVE_SHEETS=1 && pytest -m live_sheets -q

# OCR tests
set RUN_LIVE=1 && set RUN_LIVE_OCR=1 && pytest -m live_ocr -q

# End-to-end tests
set RUN_LIVE=1 && set RUN_LIVE_E2E=1 && set E2E_FILE_URL=https://files.slack.com/... && pytest -m live_e2e -q
```

**macOS/Linux:**
```bash
# Slack tests
RUN_LIVE=1 RUN_LIVE_SLACK=1 pytest -m live_slack -q

# Google Sheets tests
RUN_LIVE=1 RUN_LIVE_SHEETS=1 pytest -m live_sheets -q

# OCR tests
RUN_LIVE=1 RUN_LIVE_OCR=1 pytest -m live_ocr -q

# End-to-end tests
RUN_LIVE=1 RUN_LIVE_E2E=1 E2E_FILE_URL=https://files.slack.com/... pytest -m live_e2e -q
```

### Test Details

- **Slack Tests**: Send a test message to verify bot token and channel access
- **Google Sheets Tests**: Append a test row and verify it can be read back
- **OCR Tests**: Process a sample receipt image using system Tesseract
- **E2E Tests**: Process a real Slack file URL through the complete workflow

### Safety Notes

- Live tests will interact with real services and may create test data
- E2E tests require a valid Slack file URL from your workspace
- Tests are designed to be safe but review your environment before running
- All tests skip gracefully if required environment variables are not set
