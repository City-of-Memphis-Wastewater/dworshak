#!/usr/bin/env python3
# ./build_pyz.py
from __future__ import annotations
import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
import pyhabitat
from dworshak._version import __version__

# --- Configuration ---
PROJECT_NAME = "dworshak"
DIST_DIR = Path("dist") / "zipapp"
BUILD_ROOT = Path("dworshak-build")

def get_platform_tag():
    """Generates a descriptive platform tag using pyhabitat."""
    info = pyhabitat.SystemInfo()
    sys_name = info.system.lower()
    arch = info.architecture.lower()
    
    if pyhabitat.on_termux():
        return f"android-{arch}-termux"
    return f"{sys_name}-{arch}"

def run_command(cmd, env=None):
    """Run command with printing and environment support."""
    print(f"\n$ {' '.join(cmd)}")
    # If no env provided, default to current os.environ
    final_env = env if env is not None else os.environ.copy()
    subprocess.run(cmd, check=True, env=final_env)

def get_custom_env():
    """Handles Fdroid Termux sandboxing by redirecting TMPDIR."""
    custom_env = os.environ.copy()
    if pyhabitat.on_termux():
        termux_tmp = Path.home() / ".tmp"
        termux_tmp.mkdir(exist_ok=True)
        custom_env["TMPDIR"] = str(termux_tmp)
        print(f"Termux detected: Redirecting TMPDIR to {termux_tmp}")
    return custom_env

def run_build():
    print(f"--- PYZ Build (uv-powered) ---")

    if BUILD_ROOT.exists():
        shutil.rmtree(BUILD_ROOT)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    custom_env = get_custom_env()

    # 1. Build the Wheel
    print("\n1. Building Project Wheel...")
    run_command(["uv", "build", "--wheel", "--out-dir", str(DIST_DIR)], env=custom_env)

    wheels = sorted(DIST_DIR.glob(f"{PROJECT_NAME}-*.whl"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not wheels:
        raise FileNotFoundError("No wheel found.")
    wheel_path = wheels[0]

    # 2. Install dependencies + the wheel into the BUILD_ROOT
    # FIX: Removed --no-deps. We want the ZipApp to be portable!
    print(f"\n2. Staging wheel and dependencies...")
    run_command([
        "uv", "pip", "install",
        f"{wheel_path}[crypto]",
        "--target", str(BUILD_ROOT),
    ], env=custom_env)

    # 3. Packaging ZipApp
    platform_tag = get_platform_tag()
    output_filename = f"{PROJECT_NAME}-{__version__}-{platform_tag}.pyz"
    output_pyz = DIST_DIR / output_filename

    # FIX: Point to the actual Typer entrypoint. 
    # Since your pyproject.toml says: dworshak = "dworshak.cli:app"
    # Zipapp needs a function call, so we use a string that calls .app()
    
    run_command([
        sys.executable, "-m", "zipapp",
        str(BUILD_ROOT),
        "-o", str(output_pyz),
        "-m", "dworshak.cli:app", 
        "-p", "/usr/bin/env python3"
    ])

    output_pyz.chmod(0o755)
    shutil.rmtree(BUILD_ROOT)
    print(f"\n✅ Build successful! Portable PYZ: {output_pyz.resolve()}")
    
if __name__ == "__main__":
    run_build()
