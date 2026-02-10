#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Build a portable dworshak PYZ using shiv.

Policy:
- Desktop platforms: bundle the 'crypto' extra
- Termux: do NOT bundle cryptography
  (system python-cryptography via `pkg install python-cryptography` is used)
"""

from __future__ import annotations

import os
import sys
import shutil
import subprocess
from pathlib import Path

import pyhabitat
from dworshak._version import __version__

# -------
# Configuration
# -------

PROJECT_NAME = "dworshak"
ENTRY_POINT = "dworshak.cli:app"

DIST_DIR = Path("dist") / "zipapp"
DIST_DIR.mkdir(parents=True, exist_ok=True)

# -------
# Helpers
# -------

def run(cmd: list[str], env: dict | None = None) -> None:
    """Run a command with echo."""
    print(f"\n$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, env=env or os.environ.copy())


def build_wheel() -> None:
    """Build the project wheel using uv."""
    env = os.environ.copy()

    if pyhabitat.on_termux():
        # Work around Termux TMPDIR restrictions
        tmp = Path.home() / ".tmp"
        tmp.mkdir(exist_ok=True)
        env["TMPDIR"] = str(tmp)
        print(f"Termux detected: TMPDIR set to {tmp}")

    run(
        [
            "uv",
            "build",
            "--wheel",
            "--sdist",
            "--out-dir",
            str(DIST_DIR),
        ],
        env=env,
    )


def find_latest_wheel() -> Path:
    """Return the most recently built dworshak wheel."""
    wheels = sorted(
        DIST_DIR.glob(f"{PROJECT_NAME}-*.whl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not wheels:
        raise RuntimeError("No wheel produced")
    return wheels[0]


def crypto_extras_for_build() -> list[str]:
    """
    Decide whether to bundle cryptography.

    Termux:
      - Do NOT bundle
      - Expect system python-cryptography if needed

    Elsewhere:
      - Bundle 'crypto' extra
    """
    if pyhabitat.on_termux():
        print(
            "Termux build: cryptography will NOT be bundled\n"
            "→ Install with: pkg install python-cryptography"
        )
        return []
    return ["crypto"]


def platform_tag() -> str:
    """Generate a descriptive platform tag."""
    if pyhabitat.on_termux():
        return "android-termux"

    info = pyhabitat.SystemInfo()
    return f"{info.system.lower()}-{info.architecture.lower()}"

# -------
# Build
# -------

def build_pyz() -> None:
    build_wheel()
    wheel_path = find_latest_wheel()

    extras = crypto_extras_for_build()
    wheel_spec = str(wheel_path)

    if extras:
        wheel_spec += f"[{','.join(extras)}]"

    pyz_name = f"{PROJECT_NAME}-{__version__}-{platform_tag()}.pyz"
    output_path = DIST_DIR / pyz_name

    # clean up intermediate packaging
    if output_path.exists():
        output_path.unlink()

    run(
        [
            "shiv",
            "-o",
            str(output_path),
            "-e",
            ENTRY_POINT,
            "-p",
            "/usr/bin/env python3",
            "--compressed",
            "--no-cache",
            wheel_spec,
        ]
    )

    output_path.chmod(0o755)

    # wheel gwneration for upload is now handled separwtely in build_pyz.yml, so we should unlink here.
    # Cleanup temporary wheel (suppress to include wheel in build.yml
    try:
        wheel_path.unlink()
    except OSError:
        pass

    print(f"\n✅ Build successful: {output_path.resolve()}")

# -------

if __name__ == "__main__":
    build_pyz()
