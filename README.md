# Dworshak  🌊

**Dworshak** a cross-platform credential management solution.
It is a [sister project](#sister-project-dworshak-access) of the `dworshak-access` library.

---

### Quick Start

```bash
# Install the CLI (for most environments)
pipx install "dworshak[crypto]"

# Bootstrap the security layer
dworshak setup

# Register your first API
dworshak store --service rjn_api --item username

```

---

`dworshak --help`:
![Screenshot of the dworshak CLI Tree Help](https://raw.githubusercontent.com/City-of-Memphis-Wastewater/dworshak/main/assets/dworshak_cli_v1.1.15_help.png)


See the Help Tree by unlocking the helptree CLI command, using the DEV_TYPER_HELP_TREE env var.

```
dworshak helptree
```

![Screenshot of the dworshak CLI Tree Help](https://raw.githubusercontent.com/City-of-Memphis-Wastewater/dworshak/main/assets/dworshak_cli_v1.1.15_helptree.png)

---

<a id="sister-project-dworshak-access"></a>
## Sister Project: 
Library: `dworshak-access` 

GitHub: https://github.com/City-of-Memphis-Wastewater/dworshak-access 

PyPI: https://pypi.org/project/dworshak-access/ 

```
pip install dworshak-access
# or,  uv add dworshak-access
```

---

## 🏗  The Ultimate Vision
To become a stable credential management tool for scripting the flow of Emerson Ovation data and related APIs, supporting multiple projects in and beyond at the Maxson Wastewater Treatment Plant.

* **The Method:** "Do one boring thing well." Use Industry-standard AES (Fernet) encryption  to manage a local `~/.dworshak/` directory which includes a `.key` file, a `vault.db` encrypted credential file, and a `config.json` file for controlling defaults.

<!--## ⚖️ User Stories-->

## 🚀 Attributes
- **Secure Vault:** Fernet-encrypted SQLite storage for API credentials.
- **Root of Trust:** A local `.key` file architecture that works identically on Windows and Termux.
- **CLI Entry:** A `typer`-based interface for setup and credential management.

---

## Typical installation

```
pipx install "dworshak[crypto]"
```

## Termux installation

```
pkg install python-cryptography
pipx install dworshak --system-site-packages
```

## iSH Apline installation

```
apk add py3-cryptography 
pipx install dworshak --system-site-packages

```
