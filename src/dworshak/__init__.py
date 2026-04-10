# src/*/__init__.pt
"""
This is not the happy path. 
dworshak is not expected to be used programmatically. 
dworshak is for cli usage only, pipx installed.
Include dworshak-prompt programmatically in your project, and then you can also import dworshak_secret.
Or use the dwroshak_prompt.setup_dworshak_managers() function to return the various manager instances in a dictionary. 
"""

from __future__ import annotations
"""
from dworshak_secret import DworshakSecret
from dworshak_config import DworshakConfig
from dworshak_env import DworshakEnv
from dworshak_prompt import Obtain, PromptMode
"""

__all__ = [
    "DworshakConfig",
    "DworshakSecret",
    "DworshakEnv",
    "Obtain",
    "PromptMode",
    "ask"
]

def __getattr__(name):
    if name == "DworshakConfig":
        from dworshak_config import DworshakConfig
        return DworshakConfig

    if name == "DworshakSecret":
        from dworshak_secret import DworshakSecret
        return DworshakSecret

    if name == "DworshakEnv":
        from dworshak_env import DworshakEnv
        return DworshakEnv

    if name == "ask":
        from dworshak_prompt import dworshak_ask
        return dworshak_ask

    if name == "PromptMode":
        from dworshak_prompt import PromptMode
        return PromptMode

    if name == "Obtain":
        from dworshak_prompt import Obtain
        return Obtain

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __dir__():
    return sorted(__all__ + [
        "__all__", "__builtins__", "__cached__", "__doc__", "__file__",
        "__getattr__", "__loader__", "__name__", "__package__", "__path__", "__spec__"
    ])
