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

"""
from dworshak_secret import (
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
"""

from dworshak_secret import cli as secret_cli
from dworshak_config import cli as config_cli
from dworshak_env import cli as env_cli
from dworshak_prompt import cli as prompt_cli

from ._version import __version__
from .logging_setup import configure_root_logging_for_application

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

# Create the sub-apps
secret_app = secret_cli.app
config_app = config_cli.app
env_app = env_cli.app
prompt_app = prompt_cli.app

# Add them to the main app
app.add_typer(secret_app, name="secret")
app.add_typer(prompt_app, name="prompt")
app.add_typer(config_app, name="config")
app.add_typer(env_app, name="env")

console = Console()

add_typer_helptree(app=app, console=console, version = __version__,hidden=False)

@app.callback(invoke_without_command=True,no_args_is_help=True)
def main(ctx: typer.Context,
    version: Optional[bool] = typer.Option(None, "--version", is_flag=True, help="Show the version."),
    debug: bool = typer.Option(False, "--debug", "-d", is_flag=True, help="Enable diagnostic logging."),
    verbose: bool = typer.Option(False, "--verbose", "-v", is_flag=True, help="Enable detail logging.")
    ):
    """
    Enable --version
    """
    if version:
        typer.echo(__version__)
        raise typer.Exit(code=0)
    configure_root_logging_for_application(debug, verbose)
    
@app.command(hidden=True)
def setup():
    """Initialize credential vault (hidden shortcut)."""
    os.system("dworshak secret vault setup")
    
if __name__ == "__main__":
    app()
