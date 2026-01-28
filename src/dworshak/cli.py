# src/dworshak/cli.py
from __future__ import annotations
import typer
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pathlib import Path
from typing import Optional
from typer_helptree import add_typer_helptree

from dworshak_access import (
    initialize_vault,
    store_secret,
    get_secret,
    remove_secret,
    list_credentials,
    check_vault,
    export_vault,
    import_records,
    backup_vault,
    rotate_key
)

from dworshak.version_info import get_version

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
        typer.echo(get_version())
        raise typer.Exit(code=0)
        

@app.command()
def setup():
    """Initialize vault and encryption key."""
    initialize_vault()
    console.print(Panel.fit("Vault initialized successfully!", title="Success"))


@app.command()
def store(
    service: str = typer.Option(..., "--service", "-s", prompt=True, help="Service name"),
    item: str = typer.Option(..., "--item", "-i", prompt=True),
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
def get(service: str = typer.Option(..., "--service", "-s", prompt=True),
    item: str = typer.Option(..., "--item", "-i", prompt=True),
    fail: bool = typer.Option(False, "--fail", help="Raise error if missing"),
    value_only: bool = typer.Option(False, "--value-only", help="Only print the secret value") 
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
    elif value_only:
        typer.echo(secret, nl=False) # nl=False prevents trailing newlines
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
    if not typer.confirm(
        f"Are you sure you want to remove {service}/{item}?",
        default=False,  # ← [y/N] style — safe default
    ):
        console.print("[yellow]⛔ Operation cancelled.[/yellow]")
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
    table.add_column("Item", style="green")
    for service, item in creds:
        table.add_row(service, item)
    console.print(table)

@app.command()
def health():
    """Check vault health."""
    status = check_vault()
    #console.print(f"[bold]{status.message}[/bold] (root={status.root_path})")
    console.print(status)

@app.command()
def export(
    output_path: Optional[Path] = typer.Option(
        None, 
        "--output", "-o", 
        help="Path to save the export."
    ),
    decrypt: bool = typer.Option(
        False, 
        "--decrypt", 
        is_flag=True, 
        help="Export the file with the secrets decrypted."
    ),
    yes: bool = typer.Option(
        False,
        "--yes","-y",
        is_flag=True,
        help="Export the file with the secrets decrypted."
    )
):  
    """
    Export the current vault to a JSON file.
    """
    # export_vault handles default paths internally if output_path is None
    if decrypt and not yes:
        yes = typer.confirm(
        f"Are you sure you want to decrypted secrets in the export?",
        default=False,  # ← [y/N] style — safe default
        )
    final_path = export_vault(output_path, decrypt,yes)
    
    if final_path:
        console.print(f"[green]Success![/green] Your vault has been exported to: [bold]{final_path}[/bold]")
    else:
        console.print("[red]Export failed.[/red] Check logs for details.")

@app.command(name="import") # 'import' is a reserved keyword in Python
def import_cmd(
    path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Path to the JSON file to import."
    ),
    overwrite: bool = typer.Option(
        False, 
        "--overwrite", 
        is_flag=True, 
        help="If new credentials match existing ones, overwrite them."
    )
): 
    """
    Import a properly structured JSON file into the Dworshak vault.
    """
    # import_records returns a dict of stats: {"added": x, "updated": y, "skipped": z}

    stats = import_records(path, overwrite)
    
    if stats:
        console.print(f"\n[bold]Import Summary for {path.name}:[/bold]")
        console.print(f"  [green]Added:[/green]   {stats['added']}")
        console.print(f"  [yellow]Updated:[/yellow] {stats['updated']}")
        console.print(f"  [blue]Skipped:[/blue] {stats['skipped']}")
    else:
        console.print("[red]Import failed or rejected.[/red]")


@app.command(name="rotate-key")
def rotate_key_cmd(
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        is_flag=True,
        help="Simulate the rotation without making any changes or backups",
    ),
    no_backup: bool = typer.Option(
        False,
        "--no-backup",
        is_flag=True,
        help="Skip automatic backup (advanced / dangerous; ignored in dry-run)",
    ),
):
    """Rotate the encryption key and re-encrypt all stored secrets.

    WARNING: This is a destructive operation unless --dry-run is used.
    A backup is created automatically unless --no-backup is specified.
    Use --dry-run first to preview what will happen.
    """
    success, message, affected = rotate_key(
        dry_run=dry_run,
        auto_backup=not no_backup if not dry_run else False,
    )

    if success:
        if dry_run:
            console.print("[cyan]Dry run completed – no changes were made.[/cyan]")
        else:
            console.print("[green]✔ Key rotation completed successfully.[/green]")

        console.print(message)

    else:
        console.print(f"[red]Operation failed:[/red] {message}")
        raise typer.Exit(1)

@app.command()
def backup(
    extra_suffix: str = typer.Option(
        "",
        "--suffix", "-s",
        help="Extra identifier in the filename (e.g. 'pre-import', 'manual', 'test')."
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir", "-o",
        help="Custom directory to save the backup (default: same as vault.db)."
    ),
    no_timestamp: bool = typer.Option(
        False,
        "--no-timestamp",
        is_flag=True,
        help="Omit timestamp from filename (not recommended unless you know what you're doing)."
    ),
    yes: bool = typer.Option(
        False,
        "--yes", "-y",
        is_flag=True,
        help="Skip confirmation prompt (useful in scripts or automation)."
    )
):
    """Create a timestamped backup copy of the vault database."""
    status = check_vault()
    if not status.is_valid:
        console.print(f"[red]Vault unhealthy: {status.message}[/red]")
        raise typer.Exit(1)

    # Call the library function
    backup_path = backup_vault(
        extra_suffix=extra_suffix,
        include_timestamp=not no_timestamp,
        dest_dir=output_dir,
    )

    if backup_path:
        console.print(f"[green]✔ Backup created:[/green] [bold]{backup_path}[/bold]")
    else:
        console.print("[red]Backup failed.[/red] Check vault health or disk space.")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
