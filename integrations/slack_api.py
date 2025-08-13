from __future__ import annotations

from typing import Dict, Any, Optional

import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config.settings import get_settings


class SlackClient:
	def __init__(self) -> None:
		self.settings = get_settings()
		self.client = WebClient(token=self.settings.slack_bot_token)

	def post_message(self, channel: str, text: str) -> Optional[str]:
		try:
			resp = self.client.chat_postMessage(channel=channel, text=text)
			return resp.get("ts")
		except SlackApiError:
			return None

	def download_file(self, url: str) -> bytes:
		headers = {"Authorization": f"Bearer {self.settings.slack_bot_token}"}
		r = requests.get(url, headers=headers, timeout=30)
		r.raise_for_status()
		return r.content 