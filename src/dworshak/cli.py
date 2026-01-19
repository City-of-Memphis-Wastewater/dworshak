# src/dworshak/cli.py
from __future__ import annotations
import typer
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import json

from dworshak_access import (
    initialize_vault,
    store_secret,
    get_secret,
    list_credentials,
    check_vault,
)

# Force Rich to always enable colors, even in .pyz or Termux
os.environ["FORCE_COLOR"] = "1"
os.environ["TERM"] = "xterm-256color"

app = typer.Typer(
    name="dworshak",
    help="Dworshak CLI - secure credential orchestration.",
    add_completion=False,
    invoke_without_command=True,
    no_args_is_help=True,
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
        "help_option_names": ["-h", "--help"]
    },
)

console = Console()


@app.command()
def setup():
    """Initialize vault and encryption key."""
    initialize_vault()
    console.print(Panel.fit("Vault initialized successfully!", title="Success"))


@app.command()
def register(
    service: str = typer.Option(..., prompt=True, help="Service name"),
    item: str = typer.Option(..., prompt=True),
    username: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True)
):
    """Store a new credential in the vault."""
    store_secret(service, item, username, password)
    console.print(f"[green]✔ Credential for {service}/{item} stored securely.[/green]")


@app.command()
def retrieve(service: str, item: str):
    """Retrieve a credential from the vault."""
    try:
        creds = get_secret(service, item)
        console.print(Panel(f"Username: {creds['u']}\nPassword: {creds['p']}", title=f"{service}/{item}"))
    except KeyError:
        console.print(f"[red]No credential found for {service}/{item}[/red]")


@app.command()
def list_items():
    """List all stored credentials."""
    creds = list_credentials()
    table = Table(title="Stored Credentials")
    table.add_column("Service", style="cyan")
    table.add_column("Item", style="magenta")
    for service, item in creds:
        table.add_row(service, item)
    console.print(table)


@app.command()
def health():
    """Check vault health."""
    status = check_vault()
    console.print(f"[bold]{status.message}[/bold] (root={status.root_path})")


if __name__ == "__main__":
    app()
