from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

try:  # Optional import to keep tests runnable without system Tesseract
	import pytesseract  # type: ignore
	from PIL import Image  # type: ignore
except Exception:  # pragma: no cover
	pytesseract = None  # type: ignore
	Image = None  # type: ignore

from config.settings import get_settings


def ocr_image_to_text(image_path: Path) -> str:
	if pytesseract is None or Image is None:
		raise RuntimeError("pytesseract/Pillow not available")
	settings = get_settings()
	if settings.tesseract_cmd:
		pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd
	img = Image.open(str(image_path))
	return pytesseract.image_to_string(img, lang=settings.tesseract_lang)


def ocr_image_with_confidence(image_path: Path) -> Tuple[str, Optional[float]]:
	if pytesseract is None or Image is None:
		raise RuntimeError("pytesseract/Pillow not available")
	settings = get_settings()
	if settings.tesseract_cmd:
		pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd
	img = Image.open(str(image_path))
	data = pytesseract.image_to_data(img, lang=settings.tesseract_lang, output_type=pytesseract.Output.DICT)
	text = " ".join(w for w in data.get("text", []) if w)
	confs = [int(c) for c in data.get("conf", []) if c.isdigit() and int(c) >= 0]
	avg_conf = (sum(confs) / len(confs)) if confs else None
	return text, avg_conf 