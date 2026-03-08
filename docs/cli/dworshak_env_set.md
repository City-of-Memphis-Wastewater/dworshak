# dworshak env set

```console
                                                                                   
 Usage: dworshak env set [OPTIONS] KEY VALUE                                       
                                                                                   
 Store or update a .env configuration value (single-key).                          
                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────╮
│ *    key        TEXT  The key (e.g. PORT, API_KEY). [required]                  │
│ *    value      TEXT  The value to store. [required]                            │
╰─────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────╮
│ --path       -p      PATH  Custom config file path.                             │
│ --overwrite                Overwrite existing value.                            │
│ --debug      -d            Diagnostics.                                         │
│ --verbose    -v            Details.                                             │
│ --help       -h            Show this message and exit.                          │
╰─────────────────────────────────────────────────────────────────────────────────╯

```
