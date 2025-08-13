from __future__ import annotations

from pathlib import Path
from typing import Optional

import pdfplumber
from PyPDF2 import PdfReader


def extract_pdf_text(pdf_path: Path) -> str:
	text_parts: list[str] = []
	# Try pdfplumber first
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
	try:
		reader = PdfReader(str(pdf_path))
		for page in reader.pages:
			content = page.extract_text() or ""
			if content:
				text_parts.append(content)
	except Exception:
		pass
	return "\n".join(text_parts) 