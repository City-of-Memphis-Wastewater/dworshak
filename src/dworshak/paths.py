from pathlib import Path

# --- CONFIGURATION & PATHS ---
# Standardizing on a hidden home directory for cross-platform utility (Termux/Windows)

APP_DIR = Path.home() / ".dworshak"
KEY_FILE = APP_DIR / ".key"
DB_FILE = APP_DIR / "vault.db"
CONFIG_FILE = APP_DIR / "config.json"
