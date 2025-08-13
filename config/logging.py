import sys
from pathlib import Path

from loguru import logger

from config.settings import get_settings


def setup_logging():
	settings = get_settings()
	log_file = Path(settings.log_file_path)
	log_file.parent.mkdir(parents=True, exist_ok=True)

	logger.remove()  # Remove default stderr logger
	logger.add(sys.stderr, level=settings.log_level.upper())
	logger.add(
		log_file,
		level=settings.log_level.upper(),
		rotation="10 MB",
		compression="zip",
		enqueue=True,
		backtrace=True,
		diagnose=True,
	) 