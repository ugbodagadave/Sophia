# Sophia (AI Bookkeeping Agent) - Phased Implementation Plan

This plan outlines the build in phases. Timelines are intentionally omitted. Each phase lists deliverables and explicit environment variable checkpoints you must set.

## Phase 0 — Bootstrap & Repo Hygiene
- Initialize repository structure under `bookkeeper_agent/`
- Add `agent.yaml`, `.env.sample`, `requirements.txt`, `LICENSE`, `.gitignore`
- Author `sophia_guide.md` and this plan
- Create memory-bank docs to track progress

Checkpoints:
- None (no live services yet)

## Phase 1 — Configuration & Foundations
Deliverables:
- `config/settings.py` with typed settings
- `config/connections.yaml` template
- Directory scaffolding under `tools/`, `integrations/`, `workflows/`

Env variables to set now:
- IBM watsonx: `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, `WATSONX_URL`, `GRANITE_MODEL_ID`
- Tesseract: `TESSERACT_CMD`, `TESSERACT_LANG`, `OCR_CONFIDENCE_THRESHOLD`, `IMAGE_PREPROCESSING`

## Phase 2 — Utilities & Storage
Deliverables:
- `tools/utilities/file_handler.py`, `date_parser.py`, `currency_handler.py`
- `tools/data_management/file_storage.py` (local + cloud interfaces)

Env variables required:
- Storage: `FILE_STORAGE_TYPE`, `LOCAL_STORAGE_PATH`, `CLOUD_STORAGE_BUCKET`, `PUBLIC_URL_BASE`

## Phase 3 — Document Processing
Deliverables:
- `tools/document_processing/pdf_extractor.py` (pdfplumber/PyPDF2)
- `tools/document_processing/image_preprocessor.py` (OpenCV/Pillow)
- `tools/document_processing/image_ocr.py` (pytesseract)
- `tools/document_processing/receipt_parser.py` (Granite 3.3 prompts)

Env variables required:
- OCR: `TESSERACT_CMD`, `TESSERACT_LANG`, `OCR_CONFIDENCE_THRESHOLD`, `IMAGE_PREPROCESSING`
- IBM watsonx: `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, `WATSONX_URL`, `GRANITE_MODEL_ID`

## Phase 4 — Integrations (Google & Slack)
Deliverables:
- `integrations/google_sheets.py` (read/write with retries)
- `integrations/slack_api.py` (file intake + messages)
- `tools/data_management/sheets_writer.py`, `sheets_reader.py`
- `tools/communication/slack_handler.py`, `slack_formatter.py`, `notification_sender.py`

Env variables required:
- Google: `GOOGLE_SHEETS_CREDENTIALS_PATH`, `GOOGLE_SHEETS_SPREADSHEET_ID`, `GOOGLE_SHEETS_WORKSHEET_NAME`, `GOOGLE_DRIVE_FOLDER_ID`
- Slack: `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_CHANNEL_ID`

## Phase 5 — Analysis & Categorization
Deliverables:
- `tools/analysis/expense_analyzer.py`, `category_classifier.py`, `report_generator.py`
- Templates under `data/templates/` for categories and reports

Env variables required:
- Business rules: `DEFAULT_CURRENCY`, `TIMEZONE`, `AUTO_CATEGORIZATION`

## Phase 6 — Workflows & E2E Tests
Deliverables:
- `workflows/receipt_processing_flow.py`
- `workflows/query_handling_flow.py`
- Unit/integration tests under `tests/` with sample data

Env variables required:
- Processing: `MAX_FILE_SIZE_MB`, `SUPPORTED_IMAGE_FORMATS`, `SUPPORTED_PDF_MAX_PAGES`, `PROCESSING_TIMEOUT_SECONDS`

## Phase 7 — Deployment & Monitoring
Deliverables:
- Deploy to IBM watsonx Orchestrate
- Logging/metrics wiring; optional Sentry
- Documentation updates in `docs/`

Env variables required:
- Security: `SECRET_KEY`, `JWT_SECRET_KEY`, `ENCRYPT_FILES`
- Monitoring: `LOG_LEVEL`, `LOG_FILE_PATH`, `ENABLE_PERFORMANCE_MONITORING`, `SENTRY_DSN`
- Perf: `API_RATE_LIMIT_PER_MINUTE`, `MAX_CONCURRENT_PROCESSING`, `CACHE_ENABLED`, `CACHE_TTL_SECONDS`

---
At each phase boundary, validate env variables are present in your local `.env`. Do not commit secrets. Reference `bookkeeper_agent/.env.sample` for a canonical list. 