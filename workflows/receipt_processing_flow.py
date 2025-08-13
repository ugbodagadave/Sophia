from __future__ import annotations

from tools.communication.slack_handler import handle_slack_file


def process_slack_file_url(file_url: str) -> str:
	return handle_slack_file(file_url) 