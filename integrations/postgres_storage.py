from __future__ import annotations

import os
import uuid
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from config.settings import get_settings


DDL = """
CREATE TABLE IF NOT EXISTS receipt_files (
    id UUID PRIMARY KEY,
    relative_path TEXT NOT NULL,
    content_type TEXT NOT NULL,
    data BYTEA NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""


class PostgresStorageClient:
	def __init__(self) -> None:
		self.settings = get_settings()
		self.url = self.settings.database_url
		if not self.url:
			raise ValueError("DATABASE_URL must be set for postgres storage")
		self._ensure_schema()

	def _conn(self):
		return psycopg2.connect(self.url)

	def _ensure_schema(self) -> None:
		with self._conn() as conn:
			with conn.cursor() as cur:
				cur.execute(DDL)
				conn.commit()

	def save_bytes(self, relative_path: str, data: bytes, content_type: str) -> str:
		file_id = uuid.uuid4()
		with self._conn() as conn:
			with conn.cursor() as cur:
				cur.execute(
					"INSERT INTO receipt_files (id, relative_path, content_type, data) VALUES (%s, %s, %s, %s)",
					(str(file_id), relative_path, content_type, psycopg2.Binary(data)),
				)
				conn.commit()
		# Return a logical link target (to be combined with PUBLIC_URL_BASE)
		return str(file_id)

	def build_public_link(self, file_id: str) -> Optional[str]:
		base = self.settings.public_url_base
		if not base:
			return None
		return f"{base.rstrip('/')}/files/{file_id}" 