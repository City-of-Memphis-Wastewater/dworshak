# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on Keep a Changelog.

---

## [0.1.11] – 2026-01-22
### Added:
- build_pyz.py
- pyhabitat as a dependency
- typer-helptree as a dependency
- .github/workflows/build.yml

### Removed
- dev.py (which used to have the typer help tree)

---

## [0.1.10] – 2026-01-20
### Added:
- `help-tree`
- `--version`

### BREAKING:
- CLI commands changed for ergonomics and length:
    - retrieve -> get
    - register -> store

### Fixed:
- username and password are out, secret is in

---

## [0.1.3] – 2026-01-19
### Changed:
- Now dworshak is just a CLI around dworshak-access.

---

## [0.1.2] – 2026-01-08
### Added:
- .github/workflows/ci.yml and .github/workflows/publish.yml. Now pushing to PyPI.

---

## [0.1.1] - 2026-01-07
### Changed:
- Remove uv-generated **main.py** file in root

---

## [0.1.0] - 2026-01-05
### Added
- Initial project structure for `dworshak`.
- `cli.py` with Typer support for `setup`, `register`, and `list-services`.
- Secure SQLite vault logic using Fernet encryption.
- Multi-platform support for `.key` storage in `~/.dworshak`.

### Fixed
- Credential storage risk by migrating from plaintext `.env` to encrypted SQL blobs.

---
