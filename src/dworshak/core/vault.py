"""
Credential vault CRUD operations for Dworshak.

This module provides:
- Existence checks
- Insert and update operations
- Retrieval of encrypted blobs
- Listing of stored credentials

All encryption and decryption is handled by core.security.
"""

import sqlite3
from typing import Optional, Tuple

from dworshak.paths import DB_FILE


def credential_exists(service: str, item: str) -> bool:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute(
        "SELECT 1 FROM credentials WHERE service = ? AND item = ?",
        (service, item)
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def store_credential(service: str, item: str, encrypted_blob: bytes) -> None:
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT OR REPLACE INTO credentials (service, item, encrypted_blob)"
        " VALUES (?, ?, ?)",
        (service, item, encrypted_blob)
    )
    conn.commit()
    conn.close()


def load_encrypted_credential(service: str, item: str) -> Optional[bytes]:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute(
        "SELECT encrypted_blob FROM credentials WHERE service = ? AND item = ?",
        (service, item)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def list_credentials() -> list[tuple[str, str]]:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT service, item FROM credentials")
    rows = cursor.fetchall()
    conn.close()
    return rows
