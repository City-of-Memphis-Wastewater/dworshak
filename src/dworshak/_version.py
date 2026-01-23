from importlib.metadata import version, PackageNotFoundError
from pathlib import Path

def _get_version():
    # 1. Try to get version from the installed package metadata (Production)
    try:
        return version("dworshak")
    except PackageNotFoundError:
        pass

    # 2. Fallback: Read VERSION file directly from source (Development/Repo)
    try:
        version_file = Path(__file__).parent / "VERSION"
        if version_file.exists():
            return version_file.read_text(encoding="utf-8").strip()
    except Exception:
        pass

    return "0.0.0-unknown"

__version__ = _get_version()
