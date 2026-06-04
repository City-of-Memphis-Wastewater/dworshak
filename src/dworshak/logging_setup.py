# src/dworshak/logging_setup.py
from __future__ import annotations
import logging
import sys
from rich.logging import RichHandler
from rich.console import Console
console = Console(stderr=True)

def configure_root_logging_for_application(debug: bool=False,verbose: bool=False):
    INTENT="app"
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    root_logger.setLevel(level)
    handler = RichHandler(console=console, show_time=False, show_path=debug,log_time_format="[%H:%M:%S]")
    handler.setFormatter(logging.Formatter("%(message)s"))
    root_logger.addHandler(handler)
    root_logger.debug(f"Debug logging enabled for {INTENT}.")
    root_logger.info(f"Verbose logging enabled for {INTENT}.")
