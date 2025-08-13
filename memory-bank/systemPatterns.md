# System Patterns

## Architecture Patterns
- **Orchestrator Agent**: Defined by `agent.yaml` with discrete, single-responsibility tools
- **Micro-module Tools**: Small Python modules grouped by domain (document_processing, data_management, analysis, communication, utilities)
- **Environment-driven Configuration**: All settings via `.env` through `config/settings.py`
- **Workflow Coordination**: Orchestrated flows for receipt processing and query handling

## Storage Patterns
- **Abstraction Layer**: `FileStorage` class with pluggable backends (local, PostgreSQL)
- **UUID-based File Management**: PostgreSQL uses UUIDs for file identification
- **Reference Links**: Unified file references stored in Google Sheets `Reference` column

## Integration Patterns
- **Service Account Authentication**: Google services via service account JSON
- **Bot Token Authentication**: Slack integration via bot tokens
- **Retry Mechanisms**: Tenacity-based retry/backoff for external API calls
- **Graceful Degradation**: Optional dependencies with fallback behaviors

## Processing Patterns
- **Local Processing First**: Files processed locally before storage upload
- **Heuristic + AI Enhancement**: Basic parsing with Granite AI enrichment
- **Confidence Scoring**: OCR confidence tracking for quality assessment
- **Error Handling**: User-friendly error messages with structured logging

## Communication Patterns
- **Minimal Confirmation**: Simple text confirmations in Slack (no interactive elements)
- **Reference Storage**: File links stored in sheets for accountant review
- **Block Kit Formatting**: Reserved for analytics and reporting (not user confirmations)
