from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


INVALID_FILENAME_CHARS = r"[^A-Za-z0-9._-]+"


def ensure_directory(path: Path) -> None:
	path.mkdir(parents=True, exist_ok=True)


def sanitize_filename(name: str) -> str:
	sanitized = re.sub(INVALID_FILENAME_CHARS, "_", name).strip("._")
	return sanitized or "file"


def write_bytes(destination: Path, data: bytes) -> Path:
	ensure_directory(destination.parent)
	destination.write_bytes(data)
	return destination


def copy_file(source: Path, destination: Path, overwrite: bool = False) -> Path:
	ensure_directory(destination.parent)
	if destination.exists() and not overwrite:
		raise FileExistsError(f"Destination already exists: {destination}")
	return Path(destination.write_bytes(Path(source).read_bytes()))


def build_receipt_filename(date_str: str, vendor: str, amount: str, ext: str) -> str:
	base = f"{date_str}_{vendor}_{amount}"
	return f"{sanitize_filename(base)}.{ext.lstrip('.')}" 