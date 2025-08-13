from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence


DEFAULT_FORMATS: Sequence[str] = (
	"%Y-%m-%d",
	"%m/%d/%Y",
	"%d/%m/%Y",
	"%b %d, %Y",
	"%B %d, %Y",
	"%Y/%m/%d",
)


def parse_date(text: str, formats: Sequence[str] = DEFAULT_FORMATS) -> Optional[str]:
	candidate = text.strip()
	for fmt in formats:
		try:
			return datetime.strptime(candidate, fmt).date().isoformat()
		except ValueError:
			continue
	return None 