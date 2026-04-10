# src/*/__init__.pt
"""
This is not the happy path for scripting usage of the dworshak ecosystem. 
dworshak is not expected to be used programmatically. 
dworshak is for cli usage only, pipx installed.
Include dworshak-prompt in your project, and then you can also import dworshak_secret, etc, for programmatic usage.

Another option, as of April 2026: 
dwroshak_prompt.setup_dworshak_managers() function to return the various manager instances in a dictionary. 

"""
from __future__ import annotations

__all__ = [
]
def __dir__():
    return sorted(__all__ + [
        "__all__", "__builtins__", "__cached__", "__doc__", "__file__",
        "__getattr__", "__loader__", "__name__", "__package__", "__path__", "__spec__"
    ])
