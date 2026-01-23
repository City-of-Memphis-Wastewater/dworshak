#!/usr/bin/env python3 
# SPDX-License-Identifier: MIT
# src/dworshak/version_info.py
from __future__ import annotations
from pathlib import Path

def get_version() -> str:
    """Reads the version from the VERSION file sitting in the package root."""
    try:
        # Assuming this file is in src/dworshak/version_info.py
        # and VERSION is in src/dworshak/VERSION
        version_file = Path(__file__).parent / "VERSION"
        return version_file.read_text(encoding="utf-8").strip()
    except Exception:
        # Fallback to the hardcoded _version.py if VERSION is missing (e.g. in some wheel builds)
        try:
            from ._version import __version__
            return __version__
        except ImportError:
            return "0.0.0"

__version__ = get_version()

