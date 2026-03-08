# dworshak secret vault

```console
                                                                                   
 Usage: dworshak secret vault [OPTIONS] COMMAND [ARGS]...                          
                                                                                   
 Manage the vault infrastructure and security.                                     
                                                                                   
╭─ Options ───────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                   │
╰─────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────╮
│ setup       Initialize vault and encryption key.                                │
│ health      Check vault integrity and permissions.                              │
│ export      Export the current vault to a JSON file.                            │
│ import      Import a properly structured JSON file into the Dworshak vault.     │
│ rotate-key  Rotate the encryption key and re-encrypt all stored secrets.        │
│ backup      Create a timestamped backup copy of the vault database.             │
╰─────────────────────────────────────────────────────────────────────────────────╯

```
