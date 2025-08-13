from __future__ import annotations

from tools.analysis.category_classifier import classify_expense


def test_common_merchants():
	assert classify_expense("Starbucks", "Latte") == "Dining"
	assert classify_expense("Uber", "Ride to airport") == "Transport"
	assert classify_expense("Walmart", "Groceries") == "Groceries"
	assert classify_expense("GitHub", "Subscription") == "Software"


def test_fallback_uncategorized():
	assert classify_expense("Some Unknown Vendor", None) == "Uncategorized" 