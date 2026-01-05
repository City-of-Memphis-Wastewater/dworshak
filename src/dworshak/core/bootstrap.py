"""
Bootstrap routines for establishing the Dworshak runtime environment.

This module is responsible for:
- Creating the application directory structure
- Generating and securing the master encryption key
- Initializing the SQLite credential vault
- Writing the initial configuration file

These operations are intended to run once during setup, but remain
idempotent to support repeated execution without side effects.
"""

import os
import json
import sqlite3
from cryptography.fernet import Fernet
from rich.console import Console

from dworshak.paths import APP_DIR, KEY_FILE, DB_FILE, CONFIG_FILE

console = Console()


def initialize_environment() -> None:
    """
    Establishes the Dworshak environment on the local system.

    This includes:
    - Ensuring the application directory exists
    - Creating the master key if absent
    - Initializing the credential vault
    - Creating the configuration file with stable defaults

    All operations are safe to repeat and will not overwrite existing data.
    """
    APP_DIR.mkdir(parents=True, exist_ok=True)

    _ensure_master_key()
    _ensure_vault()
    _ensure_config()


def _ensure_master_key() -> None:
    """
    Generates the master Fernet key if it does not already exist.

    The key is stored with restrictive permissions to limit access
    to the current system account.
    """
    if KEY_FILE.exists():
        return

    console.print("[yellow]Initializing Root of Trust...[/yellow]")

    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)

    # Restrict permissions: read/write for owner only
    os.chmod(KEY_FILE, 0o600)

    console.print(f"[green]✔ Master key generated at {KEY_FILE}[/green]")


def _ensure_vault() -> None:
    """
    Creates the SQLite credential vault if it does not exist.

    The schema is intentionally minimal and stable to support long-term
    compatibility across Dworshak versions.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS credentials (
            service TEXT NOT NULL,
            item TEXT NOT NULL,
            encrypted_blob BLOB NOT NULL,
            PRIMARY KEY (service, item)
        )
        """
    )
    conn.close()


def _ensure_config() -> None:
    """
    Writes the initial configuration file if absent.

    The configuration file stores user preferences only.
    Service definitions are maintained in code to ensure stability.
    """
    if CONFIG_FILE.exists():
        return

    default_config = {
        "default_service": "rjn_api"
    }

    CONFIG_FILE.write_text(json.dumps(default_config, indent=2))
    console.print(f"[green]✔ Config file created at {CONFIG_FILE}[/green]")
