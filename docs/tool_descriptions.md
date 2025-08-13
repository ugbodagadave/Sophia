# Tool Descriptions

## Utilities
- `file_handler.py`: Safe filename generation, directory management, file write/copy helpers
- `date_parser.py`: Lightweight date parsing against common formats, returns ISO date
- `currency_handler.py`: Amount normalization and formatting helpers

## Data Management
- `file_storage.py`: Storage abstraction. Local and PostgreSQL backends supported. Links are stored in the `Reference` column in Google Sheets.

## Integrations
- `integrations/google_sheets.py`: Append and read ranges from Google Sheets
- `integrations/slack_api.py`: Post messages to Slack; download files with bot token
- `integrations/postgres_storage.py`: Save and retrieve file bytes in PostgreSQL (UUID id)

## Document Processing
- `pdf_extractor.py`: Extract text from PDFs using pdfplumber with PyPDF2 fallback
- `image_preprocessor.py`: Enhance images (grayscale, median denoise, autocontrast, optional threshold)
- `image_ocr.py`: Tesseract OCR with optional average confidence score
- `receipt_parser.py`: Heuristic parsing with optional Granite enrichment

## Analysis
- `tools/analysis/expense_analyzer.py`: Aggregate spend by category, vendor, and month; compute totals and averages; utilities to map sheet rows and format a Slack-ready summary.
- `tools/analysis/category_classifier.py`: Keyword-based classifier for vendors/descriptions; Granite-backed suggestions when heuristics fail.
- `tools/analysis/report_generator.py`: Format analyzer outputs for Slack blocks; export helpers to CSV/JSON strings or save via `FileStorage`.

## Communication
- `tools/communication/slack_formatter.py`: Returns a minimal confirmation text for receipt processing and basic error text.
