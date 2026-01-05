import os
import sqlite3
import json
from pathlib import Path
from typing import Optional

import typer
from cryptography.fernet import Fernet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# --- CONFIGURATION & PATHS ---
# Standardizing on a hidden home directory for cross-platform utility (Termux/Windows)
APP_DIR = Path.home() / ".dworshak"
KEY_FILE = APP_DIR / ".key"
DB_FILE = APP_DIR / "vault.db"

app = typer.Typer(help="Dworshak: Secure API Orchestration for Infrastructure.")
console = Console()

# --- CORE SECURITY LOGIC ---

def initialize_system():
    """Ensures the application directory and master key exist."""
    APP_DIR.mkdir(parents=True, exist_ok=True)
    
    if not KEY_FILE.exists():
        console.print("[yellow]Initializing Root of Trust...[/yellow]")
        key = Fernet.generate_key()
        KEY_FILE.write_bytes(key)
        # Set file permissions: Read/Write for owner only (Linux/Termux standard)
        os.chmod(KEY_FILE, 0o600)
        console.print(f"[green]✔ Master key generated at {KEY_FILE}[/green]")
    
    # Initialize SQLite Vault if it doesn't exist
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            service TEXT NOT NULL,
            item TEXT NOT NULL,
            encrypted_blob BLOB NOT NULL,
            PRIMARY KEY (service, item)
        )
    """)
    conn.close()

def get_fernet() -> Fernet:
    """Loads the master key from file or environment override."""
    # Check for environment override first (Standard for CI/CD/Headless)
    key = os.getenv("DWORSHAK_MASTER_KEY")
    if not key:
        if not KEY_FILE.exists():
            raise FileNotFoundError("Master key not found. Run 'dworshak setup' first.")
        key = KEY_FILE.read_bytes()
    return Fernet(key)

# --- CLI COMMANDS ---

@app.command()
def setup():
    """Bootstrap the Dworshak environment and generate security keys."""
    initialize_system()
    console.print(Panel.fit(
        "Dworshak System Initialized\n[bold green]Security Layer Active[/bold green]",
        title="Success"
    ))

@app.command()
def register(
    service: str = typer.Option(..., prompt="Service Name (e.g., rjn_api)"),
    item: str = typer.Option(..., prompt="Credential Item (e.g., primary)"),
    username: str = typer.Option(..., prompt="Username"),
    password: str = typer.Option(..., prompt="Password", hide_input=True)
):
    """Encrypt and store a new credential in the vault."""
    fernet = get_fernet()
    
    # Package credentials as JSON before encryption
    payload = json.dumps({"u": username, "p": password}).encode()
    encrypted_blob = fernet.encrypt(payload)
    
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT OR REPLACE INTO credentials (service, item, encrypted_blob) VALUES (?, ?, ?)",
        (service, item, encrypted_blob)
    )
    conn.commit()
    conn.close()
    console.print(f"[green]✔ Credential for [bold]{service}/{item}[/bold] stored securely.[/green]")

@app.command()
def list_services():
    """List all services currently stored in the vault (names only)."""
    if not DB_FILE.exists():
        console.print("[red]Vault not initialized.[/red]")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT service, item FROM credentials")
    rows = cursor.fetchall()
    conn.close()

    table = Table(title="Secure Vault Services")
    table.add_column("Service", style="cyan")
    table.add_column("Item", style="magenta")

    for row in rows:
        table.add_row(row[0], row[1])

    console.print(table)

if __name__ == "__main__":
    app()