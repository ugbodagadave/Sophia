from __future__ import annotations

from pathlib import Path
from typing import Optional

try:  # Optional import to keep tests runnable without system deps
	import pdfplumber  # type: ignore
except Exception:  # pragma: no cover
	pdfplumber = None  # type: ignore

try:
	from PyPDF2 import PdfReader  # type: ignore
except Exception:  # pragma: no cover
	PdfReader = None  # type: ignore


def extract_pdf_text(pdf_path: Path) -> str:
	text_parts: list[str] = []
	# Try pdfplumber first
	if pdfplumber is not None:
		try:
			with pdfplumber.open(str(pdf_path)) as pdf:
				for page in pdf.pages:
					content = page.extract_text() or ""
					if content:
						text_parts.append(content)
			if text_parts:
				return "\n".join(text_parts)
		except Exception:
			pass
	# Fallback to PyPDF2
	if PdfReader is not None:
		try:
			reader = PdfReader(str(pdf_path))
			for page in reader.pages:
				content = page.extract_text() or ""
				if content:
					text_parts.append(content)
		except Exception:
			pass
	return "\n".join(text_parts) 