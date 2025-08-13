from __future__ import annotations

import json
import re
from typing import Dict, Any, Optional

from config.settings import get_settings
from loguru import logger
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError

try:
	from ibm_watsonx_ai import Credentials
	from ibm_watsonx_ai.foundation_models import Model
except Exception:  # pragma: no cover - SDK import failure shouldn't break tests
	Credentials = None  # type: ignore
	Model = None  # type: ignore

from tools.utilities.date_parser import parse_date
from tools.utilities.currency_handler import normalize_amount


class _GraniteExtractionModel(BaseModel):
	date: Optional[str] = None
	vendor: Optional[str] = None
	amount: Optional[float] = None
	category: Optional[str] = None


class GraniteClient:
	def __init__(self) -> None:
		self.settings = get_settings()

	def _make_model(self) -> Optional[Model]:
		if not (self.settings.watsonx_api_key and self.settings.watsonx_project_id and self.settings.granite_model_id):
			return None
		if Credentials is None or Model is None:
			return None
		creds = Credentials(api_key=self.settings.watsonx_api_key, url=self.settings.watsonx_url)
		return Model(model_id=self.settings.granite_model_id, credentials=creds, project_id=self.settings.watsonx_project_id)

	@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=1, max=4))
	def _extract_with_retry(self, model: Model, text: str) -> Dict[str, Any]:
		prompt = (
			"You are a receipt information extractor. Given the raw text of a receipt, "
			"extract a compact JSON with keys: date (YYYY-MM-DD), vendor (string), amount (number), category (string). "
			"If a key is unknown use null. Only output the JSON object.\n\nReceipt Text:\n" + text
		)
		resp = model.generate_text(prompt=prompt)
		content = resp.get("results")[0].get("generated_text") if isinstance(resp, dict) else str(resp)
		raw = (content or "").strip()
		m = re.search(r"\{.*\}", raw, re.DOTALL)
		json_snippet = m.group(0) if m else raw
		try:
			data = json.loads(json_snippet)
		except Exception as exc:
			logger.bind(stage="granite_extract", reason="json_parse_error", raw=json_snippet[:500]).warning(
				"Failed to parse Granite JSON: {}", str(exc)
			)
			raise

		if isinstance(data, dict):
			if data.get("date") and isinstance(data.get("date"), str):
				maybe_iso = parse_date(str(data.get("date")))
				if maybe_iso:
					data["date"] = maybe_iso
			if data.get("amount") is not None and not isinstance(data.get("amount"), (int, float)):
				amt = normalize_amount(str(data.get("amount")))
				data["amount"] = float(amt) if amt is not None else None
			validated = _GraniteExtractionModel(**data).model_dump(exclude_none=True)
			return dict(validated)
		raise ValueError("Granite output was not a JSON object")

	def extract_receipt_data(self, text: str) -> Dict[str, Any]:
		"""Use Granite to extract structured fields from receipt text.
		Returns a dict possibly containing keys: date (ISO), vendor, amount (float), category.
		"""
		model = self._make_model()
		if model is None:
			return {}
		try:
			return self._extract_with_retry(model, text)
		except RetryError as exc:
			logger.bind(stage="granite_extract", reason="retry_exhausted").warning(
				"Granite extraction retries exhausted: {}", str(exc)
			)
			return {}
		except Exception as exc:
			logger.bind(stage="granite_extract", reason="validation_or_parse_error").warning(
				"Granite extraction failed; falling back to heuristics: {}", str(exc)
			)
			return {}

	@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=1, max=4))
	def _suggest_category_with_retry(self, model: Model, vendor: str, description: Optional[str] = None) -> str:
		prompt = (
			"Classify the expense category for the following vendor and description. "
			"Return only the category word or short phrase (e.g., 'Dining', 'Groceries', 'Transport', 'Software', 'Travel', 'Office Supplies', 'Utilities', 'Fees', 'Other').\n"
			f"Vendor: {vendor}\nDescription: {description or ''}"
		)
		resp = model.generate_text(prompt=prompt)
		text = resp.get("results")[0].get("generated_text").strip() if isinstance(resp, dict) else str(resp).strip()
		return text.splitlines()[0][:60] or "Uncategorized"

	def suggest_category(self, vendor: str, description: Optional[str] = None) -> str:
		model = self._make_model()
		if model is None:
			return "Uncategorized"
		try:
			return self._suggest_category_with_retry(model, vendor, description)
		except RetryError as exc:
			logger.bind(stage="granite_category", reason="retry_exhausted").warning(
				"Granite category retries exhausted: {}", str(exc)
			)
			return "Uncategorized"
		except Exception as exc:
			logger.bind(stage="granite_category", reason="model_error").warning(
				"Granite category suggestion failed; returning default: {}", str(exc)
			)
			return "Uncategorized" 