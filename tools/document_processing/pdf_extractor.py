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

# Optional OCR fallback for image-based PDFs
try:  # pragma: no cover - optional dependency
	from pdf2image import convert_from_path  # type: ignore
except Exception:
	convert_from_path = None  # type: ignore

try:  # pragma: no cover - optional dependency
	import pytesseract  # type: ignore
	from PIL import Image  # type: ignore
except Exception:
	pytesseract = None  # type: ignore
	Image = None  # type: ignore

from config.settings import get_settings


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
	if text_parts:
		return "\n".join(text_parts)

	# OCR fallback for image-based PDFs
	settings = get_settings()
	if convert_from_path is not None and pytesseract is not None and Image is not None:
		try:
			# Convert PDF to images (requires poppler installed and accessible in PATH)
			images = convert_from_path(str(pdf_path), dpi=200)
			if settings.tesseract_cmd:
				pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd
			for img in images:
				text = pytesseract.image_to_string(img, lang=settings.tesseract_lang)
				if text:
					text_parts.append(text)
			return "\n".join(text_parts)
		except Exception:
			# Silent fallback to empty string if OCR pipeline unavailable
			return ""
	# No text extracted
	return "" 