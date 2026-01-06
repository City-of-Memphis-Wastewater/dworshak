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
import click

from dworshak.paths import APP_DIR,KEY_FILE,DB_FILE,CONFIG_FILE
from dworshak.services import KNOWN_SERVICES
from dworshak.core.bootstrap import initialize_environment
from dworshak.core.security import get_fernet
from dworshak.core.vault import (
    credential_exists,
    store_credential,
)

# Force Rich to always enable colors, even when running from a .pyz bundle
os.environ["FORCE_COLOR"] = "1"
# Optional but helpful for full terminal feature detection
os.environ["TERM"] = "xterm-256color"

app = typer.Typer(
    name = "dworshak",
    help="Secure API Orchestration for Infrastructure.",
    add_completion=False,
    invoke_without_command = True,
    no_args_is_help = True,
    context_settings={"ignore_unknown_options": True,
    "allow_extra_args": True,
    "help_option_names": ["-h", "--help"]},
    )


console = Console()

# --- CLI COMMANDS ---

@app.command()
def setup():
    """Bootstrap the Dworshak environment and generate security keys."""
    #initialize_system()
    initialize_environment()
    console.print(Panel.fit(
        "Dworshak System Initialized\n[bold green]Security Layer Active[/bold green]",
        title="Success"
    ))

# def register(service: str = typer.Option("rjn_api", prompt=True)):
@app.command()
def register(
    service: str = typer.Option(
        "rjn_api",
        prompt="Service Name",
        show_default=True,
        click_type=click.Choice(KNOWN_SERVICES),),
    item: str = typer.Option(..., prompt="Credential Item (e.g., primary)"),
    username: str = typer.Option(..., prompt="Username"),
    password: str = typer.Option(..., prompt="Password", hide_input=True)
):

    """Encrypt and store a new credential in the vault."""
    # Check for existing credential
    if credential_exists(service, item):
        console.print(
            f"[yellow]A credential for {service}/{item} already exists.[/yellow]"
        )
        overwrite = typer.confirm("Overwrite?", default=False)
        if not overwrite:
            console.print("[green]Operation cancelled.[/green]")
            return

    # Encrypt the payload
    fernet = get_fernet()
    payload = json.dumps({"u": username, "p": password}).encode()
    encrypted_blob = fernet.encrypt(payload)

    store_credential(service, item, encrypted_blob)
    console.print(
        f"[green]✔ Credential for [bold]{service}/{item}[/bold] stored securely.[/green]"
    )

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
