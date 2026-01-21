#!/usr/bin/env python3 
# SPDX-License-Identifier: MIT
# src/dworshak/version_info.py
from __future__ import annotations
import re
from pathlib import Path
import sys

# --- TOML Parsing Helper ---
def find_pyproject(start: Path) -> Path | None:
    # 1. Handle PyInstaller / Frozen state
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # In PyInstaller, force-include maps to: sys._MEIPASS / package_name / data / file
        candidate = Path(sys._MEIPASS) / "dworshak" / "data" / "pyproject.toml"
        if candidate.exists():
            return candidate
        # Fallback for simple --add-data "pyproject.toml:."
        candidate = Path(sys._MEIPASS) / "pyproject.toml"
        if candidate.exists():
            return candidate

    # 4. Handle Development state (walking up the tree)
    for p in start.resolve().parents:
        candidate = p / "pyproject.toml"
        if candidate.exists():
            return candidate
        
    # 3. Handle Installed / Wheel / Shiv state (using force-include path)
    internal_path = Path(__file__).parent / "data" / "pyproject.toml"
    if internal_path.exists():
        return internal_path

    return None


def get_version_from_pyproject() -> str:
    pyproject = find_pyproject(Path(__file__))
    if not pyproject or not pyproject.exists():
        print("ERROR: pyproject.toml missing.", file=sys.stderr)
        return "0.0.0"

    text = pyproject.read_text(encoding="utf-8")
    
    # Match PEP 621 style: [project]
    project_section = re.search(r"\[project\](.*?)(?:\n\[|$)", text, re.DOTALL | re.IGNORECASE)
    if project_section:
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', project_section.group(1))
        if match: return match.group(1)

    # Match Poetry style: [tool.poetry]
    poetry_section = re.search(r"\[tool\.poetry\](.*?)(?:\n\[|$)", text, re.DOTALL | re.IGNORECASE)
    if poetry_section:
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', poetry_section.group(1))
        if match: return match.group(1)

    return "0.0.0"
