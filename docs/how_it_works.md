# How It Works

## Receipt Processing Flow (Slack → Sheets)
- Slack file URL received (image or PDF)
- File downloaded via `integrations/slack_api.py`
- File stored using `tools/data_management/file_storage.py` (local or Postgres)
- If image: `tools/document_processing/image_preprocessor.py` then `image_ocr.py` → text (+confidence)
- If PDF: `tools/document_processing/pdf_extractor.py` → text
- `tools/document_processing/receipt_parser.py` heuristics (+ Granite enrichment later)
- Expense row is mapped using `tools/data_management/sheets_writer.py` (columns from `data/templates/sheets_template.json`) and appended to Google Sheets
- The unified storage link is placed in the last column `Reference` (and in `Receipt_PDF_Link` or `Receipt_Image_Link` accordingly)
- A single Slack confirmation text is posted: “Receipt added to Google Sheet.”

## Query Handling Flow (Phase 5/6)
- Natural-language query arrives (e.g., "summary for June", "spend by category last 3 months export csv")
- `workflows/query_handling_flow.py` parses intent and optional date ranges
- Data is fetched from Google Sheets via `tools/data_management/sheets_reader.py`
- Rows converted to dicts using `tools/analysis/expense_analyzer.rows_from_values`
- Aggregations with `expense_analyzer` (by category/month/vendor, totals)
- Output formatted for Slack or exports if requested

## Error Handling
- Slack and Google errors are caught; user-friendly `:warning:` messages returned
- OCR confidence optional; can be used to trigger manual review
- Public link generation is optional and depends on storage configuration (`PUBLIC_URL_BASE` for Postgres/local)

## Configuration
- All settings flow from `.env` via `config/settings.py`
- Sheets credentials via service account; no Drive API required now
