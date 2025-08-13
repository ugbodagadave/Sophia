from __future__ import annotations

from pathlib import Path
from typing import Optional

from PIL import Image, ImageFilter, ImageOps


def preprocess_image_for_ocr(image_path: Path, threshold: bool = False) -> Path:
	img = Image.open(str(image_path))
	img = ImageOps.grayscale(img)
	img = img.filter(ImageFilter.MedianFilter(size=3))
	img = ImageOps.autocontrast(img)
	if threshold:
		img = img.point(lambda p: 255 if p > 180 else 0)
	output_path = image_path.with_name(image_path.stem + "_preprocessed" + image_path.suffix)
	img.save(str(output_path))
	return output_path 