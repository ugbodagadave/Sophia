from __future__ import annotations

from typing import Dict, Any, List


def format_receipt_summary(parsed: Dict[str, Any], confidence: float | None = None) -> str:
	# Minimal confirmation message only
	return "Receipt added to Google Sheet."


def format_error(message: str) -> str:
	return f":warning: {message}"


def build_receipt_blocks(parsed: Dict[str, Any], links: Dict[str, str] | None = None, confidence: float | None = None, processing_seconds: float | None = None) -> List[Dict[str, Any]]:
	# Blocks no longer used for end-user confirmation; return an empty list
	return []


def build_analytics_blocks(title: str, total_text: str, fields_map: Dict[str, str]) -> List[Dict[str, Any]]:
	fields = [{"type": "mrkdwn", "text": f"*{k}:*\n{v}"} for k, v in fields_map.items()]
	return [
		{"type": "header", "text": {"type": "plain_text", "text": title}},
		{"type": "section", "text": {"type": "mrkdwn", "text": total_text}},
		{"type": "section", "fields": fields},
	] 