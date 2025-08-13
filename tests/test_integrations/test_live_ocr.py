from __future__ import annotations

import os
from pathlib import Path
import pytest

from tools.document_processing.image_ocr import ocr_image_with_confidence
from config.settings import get_settings


@pytest.mark.live_ocr
def test_live_ocr_runs_on_sample_image():
	if os.getenv("RUN_LIVE") != "1" or os.getenv("RUN_LIVE_OCR") != "1":
		pytest.skip("RUN_LIVE and RUN_LIVE_OCR not set; skipping live OCR test")

	settings = get_settings()
	if not settings.tesseract_cmd:
		pytest.skip("TESSERACT_CMD not configured; skipping")

	samples_dir = Path("tests/test_data/sample_receipts")
	images = list(samples_dir.glob("**/*.*")) if samples_dir.exists() else []
	if not images:
		pytest.skip("No sample images found under tests/test_data/sample_receipts; skipping")

	text, conf = ocr_image_with_confidence(images[0])
	assert isinstance(text, str)
	assert text.strip() != "" 