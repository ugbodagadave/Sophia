# How It Works

## Receipt Processing Flow (Slack → Sheets)
- Slack file URL received (image or PDF)
- File downloaded via `integrations/slack_api.py`
- File stored using `tools/data_management/file_storage.py` (local or cloud in future)
- If image: `tools/document_processing/image_preprocessor.py` then `image_ocr.py` → text (+confidence)
- If PDF: `tools/document_processing/pdf_extractor.py` → text
- `tools/document_processing/receipt_parser.py` heuristics (+ Granite enrichment later)
- Expense row is mapped using `tools/data_management/sheets_writer.py` (columns from `data/templates/sheets_template.json`) and appended to Google Sheets
- Confirmation text formatted by `tools/communication/slack_formatter.py`

## Error Handling
- Slack and Google errors are caught; user-friendly `:warning:` messages returned
- OCR confidence optional; can be used to trigger manual review
- Storage public URL generation is optional (depends on `PUBLIC_URL_BASE`)

## Configuration
- All settings flow from `.env` via `config/settings.py`
- Connections are declared in `config/connections.yaml` for reference
