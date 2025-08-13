from __future__ import annotations

import json
import re
from typing import Dict, Any, Optional

from config.settings import get_settings

try:
	from ibm_watsonx_ai import Credentials
	from ibm_watsonx_ai.foundation_models import Model
except Exception:  # pragma: no cover - SDK import failure shouldn't break tests
	Credentials = None  # type: ignore
	Model = None  # type: ignore


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

	def extract_receipt_data(self, text: str) -> Dict[str, Any]:
		"""Use Granite to extract structured fields from receipt text.
		Returns a dict possibly containing keys: date (ISO), vendor, amount (float), category.
		"""
		model = self._make_model()
		if model is None:
			return {}
		prompt = (
			"You are a receipt information extractor. Given the raw text of a receipt, "
			"extract a compact JSON with keys: date (YYYY-MM-DD), vendor (string), amount (number), category (string). "
			"If a key is unknown use null. Only output the JSON object.\n\nReceipt Text:\n" + text
		)
		try:
			resp = model.generate_text(prompt=prompt)
			content = resp.get("results")[0].get("generated_text") if isinstance(resp, dict) else str(resp)
			raw = content.strip()
			m = re.search(r"\{.*\}", raw, re.DOTALL)
			data = json.loads(m.group(0)) if m else json.loads(raw)
			out: Dict[str, Any] = {}
			if isinstance(data, dict):
				out.update({k: v for k, v in data.items() if v is not None})
			return out
		except Exception:
			return {}

	def suggest_category(self, vendor: str, description: Optional[str] = None) -> str:
		model = self._make_model()
		if model is None:
			return "Uncategorized"
		prompt = (
			"Classify the expense category for the following vendor and description. "
			"Return only the category word or short phrase (e.g., 'Dining', 'Groceries', 'Transport', 'Software', 'Travel', 'Office Supplies', 'Utilities', 'Fees', 'Other').\n"
			f"Vendor: {vendor}\nDescription: {description or ''}"
		)
		try:
			resp = model.generate_text(prompt=prompt)
			text = resp.get("results")[0].get("generated_text").strip() if isinstance(resp, dict) else str(resp).strip()
			return text.splitlines()[0][:60] or "Uncategorized"
		except Exception:
			return "Uncategorized" 