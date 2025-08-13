from __future__ import annotations

import os
import time
import pytest

from integrations.slack_api import SlackClient


@pytest.mark.live_slack
def test_live_slack_send_message_env_gated():
	if os.getenv("RUN_LIVE") != "1" or os.getenv("RUN_LIVE_SLACK") != "1":
		pytest.skip("RUN_LIVE and RUN_LIVE_SLACK not set; skipping live Slack test")

	sc = SlackClient()
	channel = sc.settings.slack_channel_id
	if not channel or not sc.client:
		pytest.skip("Slack client not configured; skipping")

	text = f"Sophia live test ping {int(time.time())}"
	ts = None
	exc: Exception | None = None
	try:
		ts = sc.post_message(channel, text)
	except Exception as e:  # pragma: no cover - we only assert no crash
		exc = e

	# ts may be None in CI; primary assertion is that no exception was raised
	assert exc is None
	assert ts is None or isinstance(ts, str) 