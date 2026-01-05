# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on Keep a Changelog.

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
