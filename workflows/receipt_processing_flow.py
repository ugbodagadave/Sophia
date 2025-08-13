from __future__ import annotations

from tools.communication.slack_handler import handle_slack_file
from tools.communication.slack_formatter import format_error


def process_slack_file_url(file_url: str) -> str:
	if not file_url or not isinstance(file_url, str):
		return format_error("Invalid file URL.")
	try:
		return handle_slack_file(file_url)
	except Exception:
		return format_error("Unhandled error during receipt processing. Check logs and configuration.") 