# Dworshak  🌊

**Dworshak** a cross-platform credential management solution.
It is a [sister project](#sister-project-dworshak-secret) of the `dworshak-secret` library.

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
<p align="center">
  <img src="https://raw.githubusercontent.com/City-of-Memphis-Wastewater/dworshak/main/assets/dworshak_cli_v1.1.15_help.png" width="100%" alt="Screenshot of the Dworshak CLI --help">
</p>

See the helptree, imported from the `typer-helptree` library.

- GitHub: https://github.com/City-of-Memphis-Wastewater/typer-helptree
- PyPI: https://pypi.org/project/typer-helptree/


```
dworshak helptree
```

<p align="center">
  <img src="https://raw.githubusercontent.com/City-of-Memphis-Wastewater/dworshak/main/assets/dworshak_v1.2.8_helptree.svg" width="100%" alt="Screenshot of the Dworshak CLI helptree">
</p> 
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
