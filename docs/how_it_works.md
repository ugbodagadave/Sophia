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
- When `SLACK_CHANNEL_ID` is set, a Block Kit confirmation is posted (header + fields + context)

## Query Handling Flow (Phase 5/6)
- Natural-language query arrives (e.g., "summary for June", "spend by category last 3 months export csv")
- `workflows/query_handling_flow.py` parses the intent and optional date ranges:
  - this month, last month, `yyyy-mm`, last N months, past N days, Q1–Q4 YYYY
- Data is fetched from Google Sheets via `tools/data_management/sheets_reader.py`
- Rows are converted to dictionaries using `tools/analysis/expense_analyzer.rows_from_values`
- Aggregations with `expense_analyzer` (by category/month/vendor, totals)
- Output is formatted for Slack using Block Kit or plain text fallback
- Optional exports: add `export csv` or `export json` to save a report under `reports/` using `FileStorage` and return a link when `PUBLIC_URL_BASE` is configured

Example (analytics):
```
User: spend by category last 2 months export csv
Bot: Report saved: https://.../reports/by_category.csv
```

## Error Handling
- Slack and Google errors are caught; user-friendly `:warning:` messages returned
- OCR confidence optional; can be used to trigger manual review
- Storage public URL generation is optional (depends on `PUBLIC_URL_BASE`)

## Configuration
- All settings flow from `.env` via `config/settings.py`
- Connections are declared in `config/connections.yaml` for reference
