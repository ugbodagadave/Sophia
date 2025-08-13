from __future__ import annotations

from tools.analysis.category_classifier import classify_expense


def test_common_merchants(monkeypatch):
	# ensure Granite isn't called for known vendors
	assert classify_expense("Starbucks", "Latte") == "Dining"
	assert classify_expense("Uber", "Ride to airport") == "Transport"
	assert classify_expense("Walmart", "Groceries") == "Groceries"
	assert classify_expense("GitHub", "Subscription") == "Software"


def test_fallback_uncategorized(monkeypatch):
	from models import granite_client as gc_mod
	# force Granite to return a deterministic response
	def fake_suggest_category(self, vendor, description=None):
		return "Uncategorized"
	monkeypatch.setattr(gc_mod.GraniteClient, "suggest_category", fake_suggest_category)
	assert classify_expense("Some Unknown Vendor", None) == "Uncategorized" 