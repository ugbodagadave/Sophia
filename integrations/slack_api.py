from __future__ import annotations

from typing import Dict, Any, Optional, List

import requests
from requests import Response
from loguru import logger

try:  # Optional dependency for testability
	from slack_sdk import WebClient  # type: ignore
	from slack_sdk.errors import SlackApiError  # type: ignore
except Exception:  # pragma: no cover
	WebClient = None  # type: ignore
	class SlackApiError(Exception):  # type: ignore
		pass

from config.settings import get_settings
from config.logging import setup_logging

setup_logging()


class SlackClient:
	def __init__(self) -> None:
		self.settings = get_settings()
		self.client = WebClient(token=self.settings.slack_bot_token) if WebClient else None

	def post_message(self, channel: str, text: str) -> Optional[str]:
		if not self.client:
			return None
		try:
			resp = self.client.chat_postMessage(channel=channel, text=text)
			return resp.get("ts")
		except SlackApiError as e:
			logger.error("Slack API error posting message: {}", e.response["error"])
			return None

	def post_blocks(self, channel: str, blocks: List[Dict[str, Any]], text: str = "") -> Optional[str]:
		"""Post Block Kit payload to Slack with optional text fallback."""
		if not self.client:
			return None
		try:
			resp = self.client.chat_postMessage(channel=channel, text=text or " ", blocks=blocks)
			return resp.get("ts")
		except SlackApiError as e:
			logger.error("Slack API error posting blocks: {}", e.response["error"])
			return None

	def download_file(self, url: str) -> Response:
		headers = {}
		# Add auth header only for Slack URLs
		if "files.slack.com" in url:
			headers["Authorization"] = f"Bearer {self.settings.slack_bot_token}"
		r = requests.get(url, headers=headers, timeout=30)
		r.raise_for_status()
		return r 