# Tool Descriptions

## Utilities
- `file_handler.py`: Safe filename generation, directory management, file write/copy helpers
- `date_parser.py`: Lightweight date parsing against common formats, returns ISO date
- `currency_handler.py`: Amount normalization and formatting helpers

## Data Management
- `file_storage.py`: Storage abstraction. Local backend implemented; cloud backends to be added (Drive/S3/Azure)

## Integrations
- `integrations/google_sheets.py`: Append and read ranges from Google Sheets
- `integrations/slack_api.py`: Post messages and blocks to Slack; download files with bot token

## Document Processing
- `pdf_extractor.py`: Extract text from PDFs using pdfplumber with PyPDF2 fallback
- `image_preprocessor.py`: Enhance images (grayscale, median denoise, autocontrast, optional threshold)
- `image_ocr.py`: Tesseract OCR with optional average confidence score
- `receipt_parser.py`: Heuristic parsing with optional Granite enrichment

## Analysis
- `tools/analysis/expense_analyzer.py`: Aggregate spend by category, vendor, and month; compute totals and averages; utilities to map sheet rows and format a Slack-ready summary.
- `tools/analysis/category_classifier.py`: Keyword-based classifier for vendors/descriptions; returns a category or `Uncategorized`; Granite-backed suggestions when heuristics fail.
- `tools/analysis/report_generator.py`: Format analyzer outputs for Slack blocks; export helpers to CSV/JSON strings or save via `FileStorage` with public link generation.

## Communication
- `tools/communication/slack_formatter.py`: Simple text formatters plus Block Kit builders for receipt confirmations and analytics (sections + fields + context).
