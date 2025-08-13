from __future__ import annotations

import json
from typing import Dict, Any

import pytest

from models.granite_client import GraniteClient


class _FakeModel:
	def __init__(self, responses: list[Dict[str, Any]]):
		self._responses = responses
		self._calls = 0

	def generate_text(self, prompt: str):
		idx = min(self._calls, len(self._responses) - 1)
		self._calls += 1
		return self._responses[idx]


def _inject_fake_model(monkeypatch, responses):
	def fake_make_model(self):
		return _FakeModel(responses)
	monkeypatch.setattr(GraniteClient, "_make_model", fake_make_model)


def _wrap_text(s: str) -> Dict[str, Any]:
	return {"results": [{"generated_text": s}]}


def test_extract_receipt_data_valid_json(monkeypatch):
	client = GraniteClient()
	payload = json.dumps({"date": "12/31/2024", "vendor": "ACME", "amount": "15.99", "category": "Dining"})
	_inject_fake_model(monkeypatch, [_wrap_text(payload)])
	out = client.extract_receipt_data("some text")
	assert out.get("vendor") == "ACME"
	assert out.get("category") == "Dining"
	assert out.get("date") == "2024-12-31"  # coerced to ISO
	assert abs(float(out.get("amount", 0.0)) - 15.99) < 0.0001


def test_extract_receipt_data_bad_json_then_retry(monkeypatch):
	client = GraniteClient()
	bad = _wrap_text("not-json at all")
	good = _wrap_text('{"date": "2024/01/05", "vendor": "Store", "amount": "10"}')
	_inject_fake_model(monkeypatch, [bad, good])
	out = client.extract_receipt_data("text")
	assert out.get("vendor") == "Store"
	assert out.get("date") == "2024-01-05"
	assert float(out.get("amount", 0.0)) == 10.0


def test_suggest_category_retry(monkeypatch):
	client = GraniteClient()
	class _ErrModel:
		_calls = 0
		def generate_text(self, prompt: str):
			if _ErrModel._calls == 0:
				_ErrModel._calls += 1
				raise RuntimeError("transient")
			return {"results": [{"generated_text": "Dining"}]}
	monkeypatch.setattr(GraniteClient, "_make_model", lambda self: _ErrModel())
	category = client.suggest_category("ACME")
	assert category.startswith("Dining") 