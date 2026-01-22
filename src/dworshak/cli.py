# src/dworshak/cli.py
from __future__ import annotations
import typer
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional
from typer_helptree import add_typer_helptree

from dworshak_access import (
    initialize_vault,
    store_secret,
    get_secret,
    remove_secret,
    list_credentials,
    check_vault,
)

from dworshak.version_info import get_version_from_pyproject # change to import from pyhabitat

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
# help-tree() command: fragile, experimental, defaults to not being included.
if os.environ.get('DEV_TYPER_HELP_TREE',0) in ('true','1'):
    add_typer_helptree(app = app, console = console)

@app.callback()
def main(ctx: typer.Context,
    version: Optional[bool] = typer.Option(
    None, "--version", is_flag=True, help="Show the version."
    )
    ):
    """
    Enable --version
    """
    if version:
        typer.echo(get_version_from_pyproject())
        raise typer.Exit(code=0)
        

@app.command()
def setup():
    """Initialize vault and encryption key."""
    initialize_vault()
    console.print(Panel.fit("Vault initialized successfully!", title="Success"))


@app.command()
def store(
    service: str = typer.Option(..., prompt=True, help="Service name"),
    item: str = typer.Option(..., prompt=True),
    secret: str = typer.Option(..., prompt=True, hide_input=True)
):
    """Store a new credential in the vault."""
    status = check_vault()
    if not status.is_valid:
        console.print(f"status.is_valid = {status.is_valid}")
        console.print(f"status.message = {status.message}")
        raise typer.Exit(code=0)
    
    store_secret(service, item, secret)
    console.print(f"[green]✔ Credential for {service}/{item} stored securely.[/green]")


@app.command()
def get(service: str = typer.Option(..., prompt=True),
    item: str = typer.Option(..., prompt=True),
    fail: bool = typer.Option(False, "--fail", help="Raise error if missing")
):
    """Retrieve a credential from the vault."""
    status = check_vault()
    if not status.is_valid:
        console.print(f"status.is_valid = {status.is_valid}")
        console.print(f"status.message = {status.message}")
        raise typer.Exit(code=0)
    
    secret = get_secret(service, item, fail=fail)
    if secret is None:
        typer.echo(f"No credential found for {service}/{item}")
    else:
        typer.echo(f"{service}/{item}: {secret}")

@app.command()
def remove(
    service: str = typer.Option(..., prompt=True, help="Service name"),
    item: str = typer.Option(..., prompt=True, help="Item/key to remove"),
    fail: bool = typer.Option(False, "--fail", help="Raise error if secret not found")
):
    """Remove a credential from the vault."""
    status = check_vault()
    if not status.is_valid:
        console.print(f"status.is_valid = {status.is_valid}")
        console.print(f"status.message = {status.message}")
        raise typer.Exit(code=0)
    
    deleted = remove_secret(service, item)
    if deleted:
        console.print(f"[green]✔ Removed credential {service}/{item}[/green]")
    else:
        if fail:
            raise KeyError(f"No credential found for {service}/{item}")
        console.print(f"[yellow]⚠ No credential found for {service}/{item}[/yellow]")


@app.command()
def list():
    """List all stored credentials."""
    status = check_vault()
    if not status.is_valid:
        console.print(f"status.is_valid = {status.is_valid}")
        console.print(f"status.message = {status.message}")
        raise typer.Exit(code=0)
    
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

