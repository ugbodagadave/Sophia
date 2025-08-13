from __future__ import annotations

from typing import Optional

from models.granite_client import GraniteClient
from config.settings import get_settings


VENDOR_KEYWORDS = {
	"Groceries": ["walmart", "aldi", "whole foods", "trader joe", "kroger", "costco", "safeway"],
	"Dining": ["mcdonald", "starbucks", "burger king", "kfc", "subway", "chipotle", "restaurant", "cafe"],
	"Transport": ["uber", "lyft", "shell", "chevron", "exxon", "bp", "metro", "parking"],
	"Software": ["microsoft", "google", "github", "slack", "notion", "dropbox", "zoom"],
	"Travel": ["hotel", "marriott", "hilton", "delta", "united", "airbnb", "booking"],
	"Office Supplies": ["staples", "office depot", "office max", "paper", "ink"],
	"Utilities": ["verizon", "at&t", "comcast", "spectrum", "electric", "water", "utility"],
}


def _heuristic_category(vendor: str, description: Optional[str]) -> Optional[str]:
	text = f"{vendor} {description or ''}".lower()
	for category, keywords in VENDOR_KEYWORDS.items():
		for kw in keywords:
			if kw in text:
				return category
	return None


def classify_expense(vendor: str, description: Optional[str] = None) -> str:
	category = _heuristic_category(vendor or "", description)
	if category:
		return category
	# Mandatory Granite-backed suggestion when heuristics fail
	client = GraniteClient()
	return client.suggest_category(vendor or "", description) or "Uncategorized" 