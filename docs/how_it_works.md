# How It Works

## Receipt Processing Flow (Slack → Sheets)

### 1. File Upload & Download
- User uploads receipt (image or PDF) to configured Slack channel
- Sophia detects file URL and downloads content via `integrations/slack_api.py`
- File content is temporarily stored in memory for processing

### 2. File Storage & Processing
- File is stored using `tools/data_management/file_storage.py`:
  - **PostgreSQL**: Files stored as BYTEA with UUID identifiers in `receipt_files` table
  - **Local**: Files saved to configured local directory structure
- Processing path determined by file type:
  - **Images**: `tools/document_processing/image_preprocessor.py` enhances image quality, then `image_ocr.py` extracts text with confidence scoring
  - **PDFs**: `tools/document_processing/pdf_extractor.py` extracts text using pdfplumber with PyPDF2 fallback

### 3. Data Extraction & AI Enhancement
- `tools/document_processing/receipt_parser.py` applies heuristic parsing:
  - Vendor name extraction from first line
  - Date parsing using multiple format recognition
  - Amount extraction using regex patterns
  - Basic categorization
- IBM Granite 3.3 AI model enriches extracted data:
  - Validates and improves parsing accuracy
  - Suggests categories when heuristics fail
  - Handles edge cases and complex receipt formats

### 4. Google Sheets Integration
- Expense data mapped using `tools/data_management/sheets_writer.py`
- Column structure defined in `data/templates/sheets_template.json`:
  - Date, Vendor, Amount, Category (core expense data)
  - Receipt_PDF_Link, Receipt_Image_Link (format-specific references)
  - Description, Payment_Method, Currency, Confidence_Score, Processed_Date (metadata)
  - **Reference** (unified file link for accountant access)
- Row appended to configured Google Sheet via service account authentication

### 5. User Confirmation
- Simple confirmation message posted to Slack: "Receipt added to Google Sheet."
- No interactive buttons or complex UI elements
- File reference available in Google Sheets for accountant review

## Query Handling Flow (Analytics & Reporting)

### 1. Natural Language Processing
- User submits query in Slack (e.g., "summary for June", "spend by category last 3 months")
- `workflows/query_handling_flow.py` parses intent and extracts date ranges:
  - Relative dates: "last month", "past 7 days", "Q2 2024"
  - Absolute dates: "2024-06", "last 3 months"
  - Export requests: "export csv", "export json"

### 2. Data Retrieval & Analysis
- Data fetched from Google Sheets via `tools/data_management/sheets_reader.py`
- Rows converted to structured dictionaries using `tools/analysis/expense_analyzer.rows_from_values`
- Analysis performed using `tools/analysis/expense_analyzer.py`:
  - **By Category**: Group expenses by category with totals
  - **By Vendor**: Group by vendor with spending patterns
  - **By Month**: Time-based analysis and trends
  - **Totals & Averages**: Overall spending statistics

### 3. Response Generation
- Results formatted for Slack using `tools/analysis/report_generator.py`
- Block Kit formatting for rich analytics displays
- Optional file exports (CSV/JSON) with public links
- Summary statistics and percentage breakdowns

## Storage Architecture

### PostgreSQL Backend (Primary)
- **Table Structure**: `receipt_files` with UUID primary keys
- **Content Storage**: BYTEA fields for binary file data
- **Metadata**: File paths, content types, creation timestamps
- **Link Generation**: UUID-based URLs when `PUBLIC_URL_BASE` configured

### Local Storage (Fallback)
- **Directory Structure**: Organized by file type (images/, pdf/)
- **File Naming**: Sanitized filenames with date/vendor/amount patterns
- **Link Generation**: HTTP URLs when `PUBLIC_URL_BASE` configured

## Error Handling & Resilience

### Graceful Degradation
- **OCR Failures**: Fallback to heuristic parsing only
- **AI Model Errors**: Continue with basic extraction
- **Storage Issues**: Retry mechanisms with exponential backoff
- **API Failures**: User-friendly error messages with `:warning:` indicators

### Quality Assurance
- **OCR Confidence**: Track confidence scores for quality assessment
- **Data Validation**: Type coercion and format normalization
- **Duplicate Detection**: Identify potential duplicate receipts
- **Audit Trail**: Complete processing history in Google Sheets

## Live Tests (Opt-in)

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
- Markers are defined in `pytest.ini`:
  - `live_slack`, `live_sheets`, `live_ocr`, `live_e2e`

## Granite Robustness

- Granite calls include retry with exponential backoff and jitter (up to 3 attempts)
- Responses are parsed for the first JSON object and validated via a schema:
  - Fields: `date`, `vendor`, `amount`, `category`
  - Coercions: date normalized to ISO using `tools.utilities.date_parser.parse_date`, amount coerced to float via `tools.utilities.currency_handler.normalize_amount`
- On validation or parsing errors:
  - Structured warnings are logged with context
  - Empty `{}` is returned so heuristic parsing dominates

## Configuration Management

### Environment Variables
- **IBM watsonx**: API key, project ID, model configuration
- **Google Services**: Service account credentials, spreadsheet ID, worksheet name
- **Slack Integration**: Bot token, channel ID, signing secret
- **Storage**: Database URL (PostgreSQL), local paths, public URL base
- **OCR Processing**: Tesseract path, language packs, confidence thresholds
- **Business Rules**: Default currency, timezone, categorization settings

### Service Authentication
- **Google Sheets**: Service account JSON with spreadsheet access
- **Slack**: Bot token with file read and message write permissions
- **PostgreSQL**: Connection string with database access
- **IBM watsonx**: API key with project access

## Performance & Scalability

### Processing Optimization
- **Local Processing**: Files processed locally before storage upload
- **Image Enhancement**: Preprocessing improves OCR accuracy
- **Parallel Processing**: Multiple files can be processed simultaneously
- **Caching**: Repeated queries cached for faster responses

### Storage Efficiency
- **Binary Storage**: Efficient BYTEA storage in PostgreSQL
- **UUID Management**: Scalable file identification system
- **Reference Links**: Minimal storage overhead for file access
- **Cleanup**: Optional file retention policies and cleanup
