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
    
# --- PyInstaller Build ---
def run_pyinstaller(exe_name: str, mode: str = "onedir"):
    setup_dirs()
    clean_previous_artifacts(exe_name, mode)

    site_pkgs = prepare_build_venv()

    #import cryptography
    #crypto_path = Path(cryptography.__file__).parent.parent.resolve()

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
        #f"--additional-hooks-dir={HOOKS_DIR_ABS}" if HOOKS_DIR_ABS.exists() else "",
        "--hidden-import", "typer",
        "--hidden-import", "typer.main",
        "--hidden-import", "typer.models",
        "--hidden-import", "click",
        "--hidden-import", "rich",
        #"--hidden-import", "cryptography",
        # Explicitly include the cryptography submodules that analysis misses
        #"--hidden-import", "cryptography.hazmat.backends.openssl.backend",
        #"--hidden-import", "cryptography.hazmat.primitives.kdf.pbkdf2",
        # Try collect-submodules instead of collect-all since it's "not a package"
        #"--collect-submodules", "cryptography",
        "--collect-all", "cryptography",
        "--collect-submodules", "dworshak",
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

def verify_cryptography_(executable_path: Path, mode: str):
    print(f"\nVerifying cryptography in {executable_path}...")
    
    if mode == "onedir":
        # Point Python to the folder containing the frozen dependencies
        lib_dir = executable_path.parent
        env = os.environ.copy()
        env["PYTHONPATH"] = str(lib_dir)
        cmd = [sys.executable, "-c", "import cryptography; print(cryptography.__version__)"]
    else:
        # For onefile, the 'hidden command' strategy above is the only reliable way
        # because the file must self-extract to run.
        cmd = [str(executable_path), "--help"] 

    try:
        result = subprocess.run(cmd, env=env if mode=="onedir" else None, capture_output=True, text=True, check=True)
        print(f"Cryptography detected: {result.stdout.strip()}")
    except Exception as e:
        print(f"Verification failed: {e}")
        sys.exit(1)

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

# --- Main ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("onedir", "onefile"), default="onedir")
    args = parser.parse_args()

    exe_name = form_dynamic_name()
    if args.mode == "onefile":
        exe_name += "-onefile"

    exe_path = run_pyinstaller(exe_name, args.mode)

    # Then pass exe_path to verify_cryptography()
    verify_cryptography(exe_path)

