# src/dworshak/cli.py
from __future__ import annotations
import typer
from dworshak_access import (
    initialize_vault,
    store_secret,
    get_secret,
    list_credentials,
    check_vault
)

app = typer.Typer(help="Dworshak CLI — secure credential orchestration")

@app.command()
def setup():
    """Initialize vault and encryption key."""
    initialize_vault()
    typer.echo("Vault initialized successfully!")

@app.command()
def register(
    service: str = typer.Option("rjn_api", help="Service name"),
    item: str = typer.Option(..., prompt="Credential item (e.g., username)"),
    username: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True)
):
    """Store a new credential in the vault."""
    store_secret(service, item + "_username", username)
    store_secret(service, item + "_password", password)
    typer.echo(f"Credential for {service}/{item} stored securely.")

@app.command()
def retrieve(service: str, item: str):
    """Retrieve a credential from the vault."""
    try:
        value = get_secret(service, item)
        typer.echo(f"{service}/{item}: {value}")
    except KeyError:
        typer.echo(f"No credential found for {service}/{item}", err=True)

@app.command()
def list_items():
    """List all stored credentials."""
    creds = list_credentials()
    for service, item in creds:
        typer.echo(f"{service}/{item}")

@app.command()
def health():
    """Check vault health."""
    status = check_vault()
    typer.echo(f"Vault status: {status.message} (root={status.root_path})")

if __name__ == "__main__":
    app()



