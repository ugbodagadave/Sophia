from __future__ import annotations

from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed

from tools.communication.slack_handler import handle_slack_file
from tools.communication.slack_formatter import format_error


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def _handle_with_retry(file_url: str) -> str:
	return handle_slack_file(file_url)


def process_slack_file_url(file_url: str) -> str:
	if not file_url or not isinstance(file_url, str):
		return format_error("Invalid file URL.")
	try:
		return _handle_with_retry(file_url)
	except Exception as exc:
		logger.exception("Receipt processing failed: {}", exc)
		return format_error("Unhandled error during receipt processing. Check logs and configuration.") 