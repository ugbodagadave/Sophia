# Sophia (AI Bookkeeping Agent) - Build & Operations Guide

This guide walks you through setting up, developing, and operating the AI Bookkeeping Agent (Sophia) using IBM watsonx Orchestrate, IBM Granite 3.3, and Tesseract OCR. It covers local development, environment configuration, integrations (Slack + Google Sheets), and workflows.

## 1) What You’re Building
- **Agent**: IBM watsonx Orchestrate agent orchestrating tools to process receipts and answer expense queries
- **Model**: IBM Granite 3.3 instruct
- **OCR**: Tesseract OCR with preprocessing for higher accuracy
- **Channels**: Slack (file uploads + Q&A)
- **Storage**: Google Sheets as the source of truth; optional Drive/S3 for file links

Project repository: [Sophia on GitHub](https://github.com/ugbodagadave/Sophia)

## 2) Architecture Overview
- `agent.yaml` defines agent name, model, instructions, and registered tools
- Tools are implemented as small Python modules grouped by domain (document_processing, data_management, analysis, communication, utilities)
- Integrations for Google Sheets, Slack, and IBM watsonx live in `integrations/`
- Workflows coordinate tools for receipt processing and query handling
- Configuration is provided via environment variables and `config/settings.py`

## 3) Prerequisites
- Python 3.10+
- Windows 10/11 with PowerShell
- Git configured with access to GitHub
- Tesseract OCR installed and added to PATH (or configure `TESSERACT_CMD`)
- IBM watsonx access (API key, project ID)
- Google Cloud Service Account (Sheets/Drive)
- Slack App (bot + app token + signing secret)

## 4) Local Setup
1. Clone repository and enter directory
2. Create virtual environment and activate
3. Install dependencies
4. Copy `.env.sample` → `.env` and fill values
5. Verify Tesseract is reachable
6. Run quick smoke checks

Example commands (PowerShell):
```powershell
python -m venv .venv; . .venv\Scripts\Activate.ps1; pip install -r bookkeeper_agent\requirements.txt
Copy-Item bookkeeper_agent\.env.sample .env
# Verify tesseract
$env:TESSERACT_CMD = (Get-Command tesseract).Source
```

## 5) Environment Variables
Configure variables listed in `bookkeeper_agent/.env.sample`. Key ones:
- IBM watsonx: `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, `WATSONX_URL`, `GRANITE_MODEL_ID`
- Google: `GOOGLE_SHEETS_CREDENTIALS_PATH`, `GOOGLE_SHEETS_SPREADSHEET_ID`, `GOOGLE_SHEETS_WORKSHEET_NAME`, `GOOGLE_DRIVE_FOLDER_ID`
- Slack: `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_CHANNEL_ID`
- OCR: `TESSERACT_CMD`, `TESSERACT_LANG`, `OCR_CONFIDENCE_THRESHOLD`, `IMAGE_PREPROCESSING`
- Storage: `FILE_STORAGE_TYPE`, `LOCAL_STORAGE_PATH`, `CLOUD_STORAGE_BUCKET`, `PUBLIC_URL_BASE`

## 6) Key Files
- `bookkeeper_agent/agent.yaml`: Agent config, tools, channels
- `bookkeeper_agent/config/settings.py`: Central config loader via env vars
- `bookkeeper_agent/config/connections.yaml`: External service handles (values from env)
- `bookkeeper_agent/tools/*`: Tool implementations (to be filled incrementally)
- `bookkeeper_agent/integrations/*`: API clients and wrappers
- `bookkeeper_agent/workflows/*`: Orchestrated flows (receipt processing, Q&A)

## 7) Installing Tesseract OCR (Windows)
- Download installer from official source
- During install, check “Add to PATH”
- If not on PATH, set `TESSERACT_CMD` in `.env` to full path (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`)

## 8) Development Workflow
- Build tools in isolation; add unit tests under `bookkeeper_agent/tests`
- Wire tools into `agent.yaml`
- Run end-to-end workflows locally using CLI scaffolding (to be added)
- Deploy to IBM watsonx Orchestrate when stable

## 9) Security & Compliance
- Never commit secrets; use `.env` and secure secret storage
- Validate incoming files (MIME, size limits)
- Restrict Sheets sharing
- Log sensitive data minimally; redact tokens

## 10) Troubleshooting
- OCR low accuracy: enable preprocessing, increase contrast, deskew
- Slack file download failures: check scopes and file permissions
- Sheets write errors: verify service account access and worksheet name
- IBM watsonx model errors: confirm project, region URL, and model ID

---
This guide is the single source for local setup and operations. For phased implementation details, see `sophia-plan.md`. 