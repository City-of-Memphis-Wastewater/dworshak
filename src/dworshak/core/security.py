"""
Security utilities for Dworshak.

This module provides:
- Loading of the master Fernet key
- Construction of Fernet instances for encryption and decryption

Environment overrides are supported to enable automated or headless
execution environments such as CI pipelines or scheduled tasks.
"""

import os
from cryptography.fernet import Fernet

from dworshak.paths import KEY_FILE


def get_fernet() -> Fernet:
    """
    Returns a Fernet instance using the master key.

    The key is loaded from:
    1. The DWORSHAK_MASTER_KEY environment variable, if present
    2. The .key file in the application directory

    Raises:
        FileNotFoundError: if no key is available from either source.
    """
    key_override = os.getenv("DWORSHAK_MASTER_KEY")

    if key_override:
        return Fernet(key_override.encode())

    if not KEY_FILE.exists():
        raise FileNotFoundError(
            "Master key not found. Run 'dworshak setup' to initialize the environment."
        )

    key_bytes = KEY_FILE.read_bytes()
    return Fernet(key_bytes)
