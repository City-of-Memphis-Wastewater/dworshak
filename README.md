# Dworshak  🌊

`dworshak` is a cross-platform credential and config management solution. 
There are options to manage encrypted cresentials, store plaintext config to JSON, or to leverage traditional Pythonic `.env` files.
`dworshak` is the CLI layer which allows your to edit and inspect values which you can also obtain programatically by using the wider `dworshak` ecosystem.

---

### Quick Start

```bash
# Install the CLI (for most environments)
pipx install "dworshak[crypto]"

# Bootstrap the security layer
dworshak setup

# Register your first API
dworshak secret set "rjn_api"  "username"

# -> You will then be prompted, 
#    with the input characters securely hidden.

```

---


```
dworshak helptree
```

<p align="center">
  <img src="https://raw.githubusercontent.com/City-of-Memphis-Wastewater/dworshak/main/assets/dworshak_v1.2.8_helptree.svg" width="100%" alt="Screenshot of the Dworshak CLI helptree">
</p> 

`helptree` is Typer utility, imported from the `typer-helptree` library.

- GitHub: https://github.com/City-of-Memphis-Wastewater/typer-helptree
- PyPI: https://pypi.org/project/typer-helptree/

---

<a id="sister-project-dworshak-secret"></a>

## Sister Projects in the Dworshak Ecosystem

* **CLI/Orchestrator:** [dworshak](https://github.com/City-of-Memphis-Wastewater/dworshak)
* **Interactive UI:** [dworshak-prompt](https://github.com/City-of-Memphis-Wastewater/dworshak-prompt)
* **Secrets Storage:** [dworshak-secret](https://github.com/City-of-Memphis-Wastewater/dworshak-secret)
* **Plaintext Pathed Configs:** [dworshak-secret](https://github.com/City-of-Memphis-Wastewater/dworshak-config)
* **Classic .env Injection:** [dworshak-secret](https://github.com/City-of-Memphis-Wastewater/dworshak-env)

```python
pipx install dworshak
pip install dworshak-secret
pip install dworshak-config
pip install dworshak-env
pip install dworshak-prompt

```

---

## 🏗  The Ultimate Vision
To become a stable credential management tool for scripting the flow of Emerson Ovation data and related APIs, supporting multiple projects in and beyond at the Maxson Wastewater Treatment Plant.

Furthmore, we want to offer Python developers a seamless configuration management experience that they can enjoy for years to come, on all of their devices.

* **The Secret Sauce Behind** `dworshk-secret`: Use Industry-standard AES (Fernet) encryption  to manage a local `~/.dworshak/` directory which includes a `.key` file, a `vault.db` encrypted credential file, and a `config.json` file for controlling defaults.

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
