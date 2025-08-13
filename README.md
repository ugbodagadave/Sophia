# Sophia - AI-Powered Bookkeeping Agent

Sophia is an intelligent bookkeeping assistant that automates expense tracking by processing receipts uploaded to Slack. Using IBM Granite AI and Tesseract OCR, Sophia extracts expense data and stores it in Google Sheets with file references for easy accountant review.

## 🚀 Features

- **Automated Receipt Processing**: Upload images or PDFs to Slack for instant processing
- **AI-Powered Extraction**: IBM Granite 3.3 AI enhances parsing accuracy
- **OCR Technology**: Tesseract OCR with image preprocessing for better text recognition
- **Secure Storage**: PostgreSQL database for file storage with UUID management
- **Google Sheets Integration**: Automatic expense data entry with file references
- **Simple User Experience**: Just upload and get confirmation - no complex workflows
- **Analytics & Reporting**: Query expense data with natural language
- **Live Testing**: Comprehensive integration tests with opt-in environment flags

## 📋 Prerequisites

- Python 3.10 or higher
- Tesseract OCR installed and configured
- IBM watsonx account with Granite 3.3 access
- Google Cloud service account with Sheets API access
- Slack app with bot token and file permissions
- PostgreSQL database (optional - local storage available)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ugbodagadave/Sophia.git
   cd Sophia
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.sample .env
   # Edit .env with your configuration
   ```

## ⚙️ Configuration

Create a `.env` file with the following variables:

### IBM Watsonx Configuration
```
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-3-3-8b-instruct
```

### Google Services
```
GOOGLE_SHEETS_CREDENTIALS_PATH=./config/google-credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_SHEETS_WORKSHEET_NAME=Expenses
```

### Slack Integration
```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
SLACK_SIGNING_SECRET=your_signing_secret
SLACK_CHANNEL_ID=your_channel_id
```

### Storage Configuration
```
FILE_STORAGE_TYPE=postgres  # or 'local'
DATABASE_URL=postgresql://user:password@host:port/database
LOCAL_STORAGE_PATH=./data/file_storage/receipts/
PUBLIC_URL_BASE=https://your-domain.com  # optional
```

### OCR Configuration
```
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
TESSERACT_LANG=eng
OCR_CONFIDENCE_THRESHOLD=70
IMAGE_PREPROCESSING=true
```

### Processing Settings
```
MAX_FILE_SIZE_MB=10
SUPPORTED_IMAGE_FORMATS=jpg,jpeg,png,tiff,bmp
SUPPORTED_PDF_MAX_PAGES=5
PROCESSING_TIMEOUT_SECONDS=30
```

### Business Rules
```
DEFAULT_CURRENCY=USD
TIMEZONE=America/New_York
AUTO_CATEGORIZATION=true
DUPLICATE_DETECTION=true
```

## 🚀 Usage

### Receipt Processing
1. Upload a receipt (image or PDF) to your configured Slack channel
2. Sophia automatically processes the file and extracts expense data
3. Data is stored in Google Sheets with a file reference
4. You receive a confirmation: "Receipt added to Google Sheet."

### Querying Expenses
Ask questions in Slack like:
- "summary for June"
- "spend by category last 3 months"
- "top vendors this month"
- "export csv for Q2 2024"

## 🧪 Testing

### Unit Tests (Default)
Run the test suite:
```bash
python -m pytest
```

Run specific test categories:
```bash
# Unit tests only
python -m pytest tests/ -v

# Integration tests
python -m pytest tests/test_integrations/ -v

# Workflow tests
python -m pytest tests/test_workflows/ -v
```

### Live Integration Tests (Opt-in)

Sophia includes comprehensive live integration tests that can test against real services. These tests are **disabled by default** and require specific environment variables to be set.

#### Environment Variables for Live Tests

**Global Live Test Flag:**
```
RUN_LIVE=1
```

**Slack Live Tests:**
```
RUN_LIVE_SLACK=1
SLACK_BOT_TOKEN=xoxb-your-bot-token
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

#### Running Live Tests

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

#### Live Test Details

- **Slack Tests**: Send a test message to verify bot token and channel access
- **Google Sheets Tests**: Append a test row and verify it can be read back
- **OCR Tests**: Process a sample receipt image using system Tesseract
- **E2E Tests**: Process a real Slack file URL through the complete workflow

#### Safety Notes

- Live tests will interact with real services and may create test data
- E2E tests require a valid Slack file URL from your workspace
- Tests are designed to be safe but review your environment before running
- All tests skip gracefully if required environment variables are not set

## 📁 Project Structure

```
Sophia/
├── config/                 # Configuration files
├── data/                   # Templates and schemas
├── docs/                   # Documentation
├── integrations/           # External service clients
├── memory-bank/           # Project context and progress
├── models/                # AI model integration
├── tools/                 # Core processing tools
│   ├── analysis/          # Data analysis and reporting
│   ├── communication/     # Slack messaging
│   ├── data_management/   # Storage and sheets integration
│   ├── document_processing/ # OCR and PDF processing
│   └── utilities/         # Helper functions
├── workflows/             # End-to-end process flows
└── tests/                 # Test suite
```

## 🔧 Development

### Key Components

- **Document Processing**: OCR, PDF extraction, image preprocessing
- **AI Integration**: IBM Granite for receipt parsing and categorization
- **Storage**: PostgreSQL with UUID-based file management
- **Integrations**: Slack for file uploads, Google Sheets for data storage
- **Analysis**: Expense categorization, reporting, and analytics

### Architecture

- **Micro-module Design**: Small, focused tools with single responsibilities
- **Environment-driven Configuration**: All settings via environment variables
- **Graceful Degradation**: Fallback behaviors when services are unavailable
- **Retry Mechanisms**: Exponential backoff for external API calls

## 📊 Google Sheets Structure

The expense data is stored with the following columns:
- **Date**: Transaction date
- **Vendor**: Merchant or business name
- **Amount**: Transaction amount
- **Category**: Expense category (auto-assigned)
- **Receipt_PDF_Link**: PDF file reference (if applicable)
- **Receipt_Image_Link**: Image file reference (if applicable)
- **Description**: Additional transaction details
- **Payment_Method**: Payment method used
- **Currency**: Transaction currency
- **Confidence_Score**: OCR confidence percentage
- **Processed_Date**: When the receipt was processed
- **Reference**: Unified file link for accountant access

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions:
- Check the [documentation](docs/)
- Review the [how it works guide](docs/how_it_works.md)
- Open an issue on GitHub

## 🔄 Status

- **Phase 6**: ✅ Storage & User Experience (Completed)
- **Next**: Phase 7 - Deployment to IBM watsonx Orchestrate

---

**Sophia** - Making expense tracking effortless with AI-powered automation. 