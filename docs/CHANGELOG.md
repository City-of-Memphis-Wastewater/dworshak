# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on Keep a Changelog.

---

## [0.1.15] – 2026-01-24
### Changed:
- Claimed compatibility with Python 3.9

---

## [0.1.15] – 2026-01-24
### Changed:
- dwroshak-access bumped to 0.1.23

### Added:
- import and export functions


---

## [0.1.14] – 2026-01-23
### Changed:
- dwroshak-access bumped to 0.1.21

---

## [0.1.13] – 2026-01-23
### Fixed:
- Versioning is now handled by editing src/dworshak/VERSION

---

## [0.1.12] – 2026-01-22
### Internal:
- Guard against edge cases like missing or malformed DB .
- Version the DB schema so that i can be checked for compatibility.
- Improve PYZ file naming to reflect the system, like pdflinkcheck, and not like pyhabitat.

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
