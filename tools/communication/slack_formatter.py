from __future__ import annotations

from typing import Dict, Any


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