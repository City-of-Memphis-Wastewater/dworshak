# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on Keep a Changelog.

---

## [1.1.5] – 2026-01-28 
### BREAKING CHANGES:
- Flat app structure converted to nested app structure, with sub apps: secret, vault, config, and prompt.
- Now dworshak exposes dworshak-secret and dworshak-prompt.
- Soon dworshak will also expose dworshak-config.
- dworshak-secret is the new name of the dworshak-acces package, for clarity

---

## [1.1.4] – 2026-01-28 
### Changed:
- Update pyproject.toml description to not use bold markers (asterisk).

---

## [1.1.3] – 2026-01-28 
### Changed:
- Update screenshots in README
- Update README installation guide and helptree call

---

## [1.1.2] – 2026-01-28 
### Changed:
- Add abbreviated flags for item and service name, -i and -s, in get and store commands.
- Add "--value-only" flag to get command, for easier var assignment in the command line.
- Add __main__ file to enable python -m dworshak
- Increase typer-helptree dependency to v0.1.10, with form add_typer_helptree(app, console, version = __version__, hidden=True)

### Internal:
- Favor flags instad of positionals, for service and item values, for get and store commands. Explicit is better than implicit, and credential management does not need to be particularly fast. Short flags -s and -i help with speed.
 
---

## [1.1.1] – 2026-01-28 
### Changed:
- Bump dworshak-access to 1.1.1.
- Magenta text in list command for Item column has been changed to green text, for visibility against PowerShell blue on a Windows 10 system.

---

## [0.1.18] – 2026-01-25
### Changed:
- Bump dworshak-access to 0.1.29.

### Internal:
- Do not state the version number of dworshak-access in the optional dependency 'crypto' section. This is a maintenance risk to keep up with the number in two places. 

---

## [0.1.17] – 2026-01-24
### Changed:
- No longer does installation include crytography. User must explicity include it as an extra, [crypto].
- Readme reflects new installation methods

### Fixed:
- bumped dworshak-access version to 0.1.28, which now is 3.9 safe by using datetime.timezone.utc instead of datetime.UTC.

---

## [0.1.16] – 2026-01-24
### Changed:
- Claimed compatibility with Python 3.9

### Added:
- backup command
- rotate-key command

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
