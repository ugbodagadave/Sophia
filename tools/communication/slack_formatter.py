from __future__ import annotations

from typing import Dict, Any, List


def format_receipt_summary(parsed: Dict[str, Any], confidence: float | None = None) -> str:
	parts = [
		"Receipt processed:",
		f"- Date: {parsed.get('date')}",
		f"- Vendor: {parsed.get('vendor')}",
		f"- Amount: {parsed.get('amount')}",
		f"- Category: {parsed.get('category')}",
	]
	if confidence is not None:
		parts.append(f"- OCR Confidence: {confidence:.1f}%")
	return "\n".join(parts)


def format_error(message: str) -> str:
	return f":warning: {message}"


def build_receipt_blocks(parsed: Dict[str, Any], links: Dict[str, str] | None = None, confidence: float | None = None, processing_seconds: float | None = None) -> List[Dict[str, Any]]:
	links = links or {}
	fields = [
		{"type": "mrkdwn", "text": f"*Vendor:*\n{parsed.get('vendor') or '-'}"},
		{"type": "mrkdwn", "text": f"*Amount:*\n{parsed.get('amount') or '-'}"},
		{"type": "mrkdwn", "text": f"*Date:*\n{parsed.get('date') or '-'}"},
		{"type": "mrkdwn", "text": f"*Category:*\n{parsed.get('category') or '-'}"},
	]
	blocks: List[Dict[str, Any]] = [
		{"type": "header", "text": {"type": "plain_text", "text": "📄 Receipt Processed"}},
		{"type": "section", "fields": fields},
	]
	context_parts: List[str] = []
	if links.get("pdf"):
		context_parts.append(f"🔗 <{links['pdf']}|Receipt PDF>")
	if links.get("image"):
		context_parts.append(f"🖼️ <{links['image']}|Receipt Image>")
	if processing_seconds is not None:
		context_parts.append(f"⚡ {processing_seconds:.1f}s")
	if confidence is not None:
		context_parts.append(f"{confidence:.0f}% confidence")
	if context_parts:
		blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": " | ".join(context_parts)}]})
	# Actions block for follow-ups
	blocks.append({
		"type": "actions",
		"elements": [
			{"type": "button", "text": {"type": "plain_text", "text": "✏️ Edit Details"}, "action_id": "edit_details"},
			{"type": "button", "style": "primary", "text": {"type": "plain_text", "text": "✅ Approve"}, "action_id": "approve"},
			{"type": "button", "style": "danger", "text": {"type": "plain_text", "text": "❌ Reject"}, "action_id": "reject"},
		]
	})
	return blocks


def build_analytics_blocks(title: str, total_text: str, fields_map: Dict[str, str]) -> List[Dict[str, Any]]:
	fields = [{"type": "mrkdwn", "text": f"*{k}:*\n{v}"} for k, v in fields_map.items()]
	return [
		{"type": "header", "text": {"type": "plain_text", "text": title}},
		{"type": "section", "text": {"type": "mrkdwn", "text": total_text}},
		{"type": "section", "fields": fields},
	] 