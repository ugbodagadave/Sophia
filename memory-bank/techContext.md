# Technical Context

## Current Architecture
- **Storage**: PostgreSQL (primary) and local file system (fallback)
- **AI/ML**: IBM Granite 3.3 for receipt parsing and categorization
- **OCR**: Tesseract with image preprocessing (OpenCV/Pillow)
- **Integrations**: Slack (file uploads, confirmations), Google Sheets (expense data)
- **Processing**: PDF extraction (pdfplumber/PyPDF2), image enhancement

## Key Technologies
- **Python 3.10+**: Core application language
- **PostgreSQL**: File storage with BYTEA and UUID management
- **IBM watsonx**: AI model hosting and inference
- **Tesseract OCR**: Text extraction from images
- **Google Sheets API**: Expense data management
- **Slack API**: File handling and messaging

## Dependencies
- **psycopg2-binary**: PostgreSQL connectivity
- **ibm-watsonx-ai**: IBM AI model integration
- **pytesseract**: OCR processing
- **google-api-python-client**: Google Sheets integration
- **slack_sdk**: Slack API integration
- **pytest**: Testing framework

## Configuration
- Environment-driven via `.env` file
- Service account authentication for Google services
- Bot token authentication for Slack
- Database URL for PostgreSQL connection
