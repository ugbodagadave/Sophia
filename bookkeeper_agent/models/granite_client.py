from __future__ import annotations

from typing import Dict, Any, Optional

from bookkeeper_agent.config.settings import get_settings


class GraniteClient:
	def __init__(self) -> None:
		self.settings = get_settings()

	def extract_receipt_data(self, text: str) -> Dict[str, Any]:
		# Placeholder: if IBM watsonx credentials are not configured, return empty
		if not self.settings.watsonx_api_key or not self.settings.watsonx_project_id:
			return {}
		# TODO: Implement real call to Granite 3.3 using ibm-watsonx-ai SDK
		# For now, return empty dict to keep offline development moving
		return {} 