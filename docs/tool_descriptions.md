# Tool Descriptions

## Utilities
- `file_handler.py`: Safe filename generation, directory management, file write/copy helpers
- `date_parser.py`: Lightweight date parsing against common formats, returns ISO date
- `currency_handler.py`: Amount normalization and formatting helpers

## Data Management
- `file_storage.py`: Storage abstraction. Local backend implemented; cloud backends to be added (Drive/S3/Azure)

## Integrations
- `integrations/google_sheets.py`: Append and read ranges from Google Sheets
- `integrations/slack_api.py`: Post messages and download files from Slack using bot token

## Document Processing
- `pdf_extractor.py`: Extract text from PDFs using pdfplumber with PyPDF2 fallback
- `image_preprocessor.py`: Enhance images (grayscale, median denoise, autocontrast, optional threshold)
- `image_ocr.py`: Tesseract OCR with optional average confidence score
- `receipt_parser.py`: Heuristic parsing with optional Granite enrichment
