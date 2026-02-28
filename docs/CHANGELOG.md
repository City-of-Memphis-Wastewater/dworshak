# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on Keep a Changelog.

---

## [1.2.12] – 2026-02-28
### Changed:
- dworshak-prompt to 0.2.24
- dworshak-secret to 1.2.11
- Change build_pyz.yml instances of manage-vault to vault.

---

## [1.2.11] – 2026-02-28
### Changed:
- Set dworshak-env dep to 0.1.5
- Set dworshak-prompt to 0.2.23
- Set dworshak-config to 0.2.4
- Update helptree svg

---

## [1.2.10] – 2026-02-26
### Changed:
- Set dworshak-secret dep to 1.2.10
- Set dworshak-prompt to 0.2.22
- Set dworshak-config to 0.2.3
- dworshak-config now has list and remove sub commands

### Internal:
- Known inconsistencies:
    - dworshak-env does not have list and remove commands
    - dworshak-prompt have --verbose and --debug commands but the other sub apps do not.
    - dworshak-config has --path flags but inconsistently have -p as an abbreviated version.
- We need to collapse down a lot of the redudancy in dworshak-prompt. Are kwargs our friend?

---

## [1.2.9] – 2026-02-17
### Changed
- Improve README.
- Stop including basic --help screenshot. It is a maintenance risk/burden.

---

## [1.2.8] – 2026-02-17
### Changed
- Set typer-helptree dep to 1.2.6
- Set dworshak-secret dep to 1.2.8
- Set dworshak-prompt to 0.2.20

### Added:
- Leveraged new `helptree --export-svg --assets` which is great (!), to handle screenshots saved to ./assets/. This is way better.

---

## [1.2.7] – 2026-02-13
### Added:
- Dummy 'typer' extra, for ecosystem consistency; i have several time tried edit other lines line 'uv add dwroshak-prompt --extra typer --extra crypto', to apply the same line for dworshak, to save typing, and then get punished with a 'typer extra does not exist'. So now it exists.

### Changed:
- Update ecosystem dependencies for CLI standardization and bug squashing.

---

## [1.2.6] – 2026-02-13
### Changed:
- Import dworshak-secret cli into cli.py. Remove redundant dead code.

### Fixed:
- typer-helptree to 0.2.5, to correct sub apps interleaved with commands, alphabetizing but not giving thw obvious recursive levels. 

### Internal:
- Screenshot asset is now firmly out of date.

---

## [1.2.4->5] – 2026-02-13
### Changed:
- Bump to v1.2.5 with nore time to reaolve dworshak-prompt 0.2.18

---

## [1.2.3] – 2026-02-13
### Changed:
- Increase dworshak_prompt to 0.2.17 and dworshak_config to 0.2.1. ConfigManager - > DworshakConfig

---

## [1.2.2] – 2026-02-13
### Fixed:
- Add '--collect-submodules' flags for all libraries in the dworshak suite to build_executable.py
 
---

## [1.2.1] – 2026-02-13
### Fixed:
- uv sync with dworshak-prompt 0.2.15 and dworshak-secret 0.2.4, which celebrate the standard dworshak ecosystem extras, typer and crypto.

### Added:
- dworshak-env

---

## [1.1.15] – 2026-02-11
### Fixed:
- Use pyhabitat.get_interp_shebang() with -p flag in shiv call in build_pyz.py.

### Changed:
- To update the screenshots, we must first update typer-helptree to see recursively into nested sub apps.

---

## [1.1.14] – 2026-02-11
### Fixed:
- Ensure build_executable.yml has uv installed
- Guard against unmatched files during upload with continue on error true.

---

## [1.1.13] – 2026-02-11 
### Changed:
- Ensure build group carries shiv for pyz.
- Zip onedir output.
- suppress checksums

---

## [1.1.11] – 2026-02-10 
### Fixed:
- Correct exe chmoding for onedir and onefile
- Generate checksums for all os matrix. 
- Ensure sanity check differentiation for windows.

---

## [1.1.10] – 2026-02-10 
### Fixed:
- Use `uv build` instead of `python -m build` in build_pyz.yml
- Remove emojis from build_*.py to allow runner success on windows action.
- chmod 0o755 in pyinstaller script for testing.

### Changed:
- Let build_pyz.yml generate the tar.gz and .whl files for upload. Use wheel.unlink in build_pyz.py so that those are not uploaded but are destroyed. 

---

## [1.1.9] – 2026-02-10 
### Added:
- pyinstaller build script and runner

### Changed:
- runner build.yml now triggers build_pyz.yml and build_executable.yml

### Internal:
- Using build_executable.py is untenable on Termux because it cannot reasonably include cryptography from source (due to time to package)

---

## [1.1.8] – 2026-02-10 
### Internal:
- Shiv is succeeding and crypto test is suceeding. 

### Fixed:
- Do not unlink the wheel in build_pyz.py, so that it can be checksummed and uploaded to release"          [dev d067d38] shiv is succeeding and crypto test is suceeding. do not unlink the wheel, so that it can be checksummed and uploaded to release.

---

## [1.1.7] – 2026-02-10 
### Changed:
- build.yml includes extra optional dep group 'build', for shiv.
- build_pyz.py uses shiv instead of zipapp.

### Internal:
- dworshak-secret inspected for PYZ inclusiomln capacity, concerning cryptography eager import.

---

## [1.1.6] – 2026-02-09 
### Fixed:
- build.yml

### Internal:
- PYZ file needs sys and arch and version info in filename.

---

## [1.1.5] – 2026-02-09 
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
