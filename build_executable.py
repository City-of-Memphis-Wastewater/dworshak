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

def prepare_build_venv() -> Path:
    """Create a temporary venv for building and return the path to its site-packages."""
    build_venv_dir = BUILD_DIR / "venv"
    print(f"Preparing isolated build environment in {build_venv_dir}...")
    
    # 1. Create the venv
    subprocess.run(["uv", "venv", str(build_venv_dir)], check=True)
    
    # Determine executable paths (Windows vs Unix)
    if IS_WINDOWS:
        bindir = build_venv_dir / "Scripts"
        python_exe = bindir / "python.exe"
    else:
        bindir = build_venv_dir / "bin"
        python_exe = bindir / "python"

    # 2. Install the project with the crypto extra and pyinstaller
    # We install '.' to get the local source, plus pyinstaller itself
    print("Installing dependencies into build venv...")
    subprocess.run([
        "uv", "pip", "install", 
        "--python", str(python_exe),
        ".[crypto]", "pyinstaller"
    ], check=True)

    # 3. Get the site-packages path from this new venv
    result = subprocess.run(
        [str(python_exe), "-c", "import site; print(site.getsitepackages()[0])"],
        capture_output=True, text=True, check=True
    )
    return Path(result.stdout.strip())

# 2. Resolve explicit paths for VERSION files
# We use a small helper to get the path from the perspective of the BUILD venv
def get_pkg_path(pkg_name):
    # We must use the venv's python to find the path, 
    # as the current script's 'importlib' won't see the venv's site-packages yet
    cmd = [str(BUILD_DIR / "venv" / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")), 
           "-c", f"import {pkg_name}; from pathlib import Path; print(Path({pkg_name}.__file__).parent)"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return Path(res.stdout.strip())
    
# --- PyInstaller Build ---
def run_pyinstaller(exe_name: str, mode: str = "onedir"):
    sep = ";" if IS_WINDOWS else ":"
    setup_dirs()
    clean_previous_artifacts(exe_name, mode)

    site_pkgs = prepare_build_venv()
    #import cryptography
    #crypto_path = Path(cryptography.__file__).parent.parent.resolve()

    # Resolve each one explicitly
    dw_path = get_pkg_path("dworshak")
    sec_path = get_pkg_path("dworshak_secret")
    env_path = get_pkg_path("dworshak_env")
    cfg_path = get_pkg_path("dworshak_config")
    pro_path = get_pkg_path("dworshak_prompt")
    
    # 2. Find the pyinstaller executable in that environment
    build_venv_bin = BUILD_DIR / "venv" / ("Scripts" if IS_WINDOWS else "bin")
    pyinstaller_bin = build_venv_bin / ("pyinstaller.exe" if IS_WINDOWS else "pyinstaller")
    
    cmd = [
        str(pyinstaller_bin),
        "--noconfirm",
        "--clean",
        f"--name={exe_name}",
        f"--paths={site_pkgs}", # Help it find the newly installed crypto
        f"--distpath={DIST_DIR_ONEFILE if mode=='onefile' else DIST_DIR_ONEDIR}",
        f"--workpath={BUILD_DIR / 'work'}",
        f"--specpath={BUILD_DIR}",
        f"--additional-hooks-dir={HOOKS_DIR_ABS}" if HOOKS_DIR_ABS.exists() else "",

        # Explicitly bundle using resolved paths
        "--add-data", f"{dw_path / 'VERSION'}{sep}dworshak",
        "--add-data", f"{sec_path / 'VERSION'}{sep}dworshak_secret",
        "--add-data", f"{env_path / 'VERSION'}{sep}dworshak_env",
        "--add-data", f"{cfg_path / 'VERSION'}{sep}dworshak_config",
        "--add-data", f"{pro_path / 'VERSION'}{sep}dworshak_prompt",

        "--hidden-import", "typer",
        "--hidden-import", "typer.main",
        "--hidden-import", "typer.models",
        "--hidden-import", "click",
        "--hidden-import", "rich",
        "--collect-all", "cryptography",
        "--collect-submodules", "dworshak",
        "--collect-submodules", "dworshak_secret",  # Added for safety
        "--collect-submodules", "dworshak_config",  # Added for safety
        "--collect-submodules", "dworshak_env",  # Added for safety
        "--collect-submodules", "dworshak_prompt",  # Ensure the prompt package is fully visible
        
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
    print(f"\nVerifying cryptography by running: {executable_path} vault health")

    try:
        # Run the actual built binary, not python -c
        result = subprocess.run(
            [str(executable_path), "vault", "health"],
            capture_output=True,
            text=True,
            check=False # We want to inspect the error code ourselves
        )
        
        # If 'Encryption is not available' is in the output, it failed
        if "Encryption is not available" in result.stderr or "ModuleNotFoundError" in result.stderr:
            print("Failed to detect cryptography in the executable!")
            print(result.stderr)
            sys.exit(1)
        else:
            print("Cryptography check passed (or at least didn't crash on imports)!")
            
    except Exception as e:
        print(f"Execution failed: {e}")
        sys.exit(1)

def zip_onedir(exe_name: str) -> Path:
    """
    Zip the contents of a PyInstaller onedir build.

    Produces:
      dist/onedir/<exe_name>.zip

    The zip contains the *contents* of:
      dist/onedir/<exe_name>/
    """
    onedir_dir = DIST_DIR_ONEDIR / exe_name
    if not onedir_dir.is_dir():
        raise RuntimeError(f"Onedir folder not found: {onedir_dir}")

    zip_path = DIST_DIR_ONEDIR / f"{exe_name}.zip"

    # Remove old zip if present
    if zip_path.exists():
        zip_path.unlink()

    print(f"Zipping onedir contents → {zip_path}")

    shutil.make_archive(
        base_name=str(zip_path.with_suffix("")),
        format="zip",
        root_dir=onedir_dir,
        base_dir=".",  # zip *contents*, not parent folder
    )

    print(f"Created zip: {zip_path.resolve()}")
    return zip_path.resolve()

# --- Main ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("onedir", "onefile"), default="onedir")
    args = parser.parse_args()

    exe_name = form_dynamic_name()
    if args.mode == "onefile":
        exe_name += "-onefile"

    exe_path = run_pyinstaller(exe_name, args.mode)
    if args.mode == "onedir":
        zip_path = zip_onedir(exe_name)
    
    # Then pass exe_path to verify_cryptography()
    verify_cryptography(exe_path)

