from __future__ import annotations

from integrations.slack_api import SlackClient
from config.settings import get_settings


def send_status(text: str) -> None:
	settings = get_settings()
	client = SlackClient()
	channel = settings.slack_channel_id or "#general"
	client.post_message(channel=channel, text=text) 