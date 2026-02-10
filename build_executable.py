#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
build_executable.py for dworshak

Builds standalone executables (onefile / onedir) using PyInstaller.
"""

from __future__ import annotations
import shutil
import subprocess
import sys
import os
from pathlib import Path
import argparse
import pyhabitat

from dworshak._version import __version__

# --- Configuration ---
PROJECT_NAME = "dworshak"
CLI_MAIN_FILE = Path("src/dworshak/cli.py")  # adjust if entry changes
DIST_DIR = Path("dist")
DIST_DIR_ONEFILE = DIST_DIR / "onefile"
DIST_DIR_ONEDIR = DIST_DIR / "onedir"
BUILD_DIR = Path("build/pyinstaller_work")
HOOKS_DIR_ABS = Path("build_assets/pyinstaller_hooks")  # optional hooks dir

IS_WINDOWS = pyhabitat.on_windows()

# --- Helpers ---

def form_dynamic_name() -> str:
    """Generate a standardized name with version, OS, arch."""
    sys_info = pyhabitat.SystemInfo()
    os_tag = sys_info.get_os_tag()
    arch = sys_info.get_arch()
    py_ver = f"py{sys.version_info.major}{sys.version_info.minor}"
    return f"{PROJECT_NAME}-{__version__}-{py_ver}-{os_tag}-{arch}"

def setup_dirs():
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR_ONEFILE.mkdir(parents=True, exist_ok=True)
    DIST_DIR_ONEDIR.mkdir(parents=True, exist_ok=True)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

def clean_previous_artifacts(exe_name: str, mode: str):
    """Clean previous builds."""
    if mode == "onedir":
        target = DIST_DIR_ONEDIR / exe_name
        if target.exists():
            shutil.rmtree(target)
    else:
        ext = ".exe" if IS_WINDOWS else ""
        target = DIST_DIR_ONEFILE / f"{exe_name}{ext}"
        if target.exists():
            target.unlink()
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

# --- PyInstaller Build ---
def run_pyinstaller(exe_name: str, mode: str = "onedir"):
    setup_dirs()
    clean_previous_artifacts(exe_name, mode)

    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--clean",
        f"--name={exe_name}",
        f"--distpath={DIST_DIR_ONEFILE if mode=='onefile' else DIST_DIR_ONEDIR}",
        f"--workpath={BUILD_DIR / 'work'}",
        f"--specpath={BUILD_DIR}",
        f"--additional-hooks-dir={HOOKS_DIR_ABS}" if HOOKS_DIR_ABS.exists() else "",
        "--hidden-import", "typer",
        "--hidden-import", "typer.main",
        "--hidden-import", "typer.models",
        "--hidden-import", "click",
        "--hidden-import", "rich",
    ]

    if mode == "onefile":
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")

    cmd.append(str(CLI_MAIN_FILE.resolve()))
    cmd = [c for c in cmd if c]  # remove empty strings

    print(f"Running PyInstaller:\n{' '.join(cmd)}")
    subprocess.run(cmd, check=True, env=os.environ.copy())

    # Determine final path
    #ext = ".exe" if IS_WINDOWS else ""
    #final_path = (DIST_DIR_ONEFILE / f"{exe_name}{ext}") if mode == "onefile" else (DIST_DIR_ONEDIR / exe_name)
    # Determine actual executable path
    ext = ".exe" if IS_WINDOWS else ""
    if mode == "onefile":
        final_path = DIST_DIR_ONEFILE / f"{exe_name}{ext}"
    else:  # onedir
        final_path = DIST_DIR_ONEDIR / exe_name / f"{exe_name}{ext}"

    print(f"\nPyInstaller build complete: {final_path.resolve()}")
    final_path.chmod(0o755)  # make executable
    return final_path.resolve()
    
# --- Post-build verification ---
def verify_cryptography(executable_path: Path):
    """Run the built executable in a subprocess and check if cryptography is importable."""
    import subprocess
    import sys

    print(f"\nVerifying cryptography in {executable_path}...")

    # Use -c to run a short Python snippet inside the frozen executable
    # For PyInstaller onefile, --version works; for onedir, use env PYTHONPATH if needed
    try:
        result = subprocess.run(
            [str(executable_path), "-c", "import cryptography; print(cryptography.__version__)"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"2cryptography detected: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print("Failed to detect cryptography in the executable!")
        print(e.stderr)
        sys.exit(1)

# --- Main ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("onedir", "onefile"), default="onedir")
    args = parser.parse_args()

    exe_name = form_dynamic_name()
    if args.mode == "onefile":
        exe_name += "-onefile"

    exe_path = run_pyinstaller(exe_name, args.mode)

    # Then pass exe_to_run to verify_cryptography()
    verify_cryptography(exe_to_run)

