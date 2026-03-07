# Vault Architecture

The **Dworshak Vault** is the central storage system for all secrets, configurations, and environment data. It is designed with security, auditability, and ease-of-use in mind, allowing users and automated processes to safely retrieve and store sensitive information.
The default path for the vault is at ~/.dworshak/vault.md, and is paired with a .key file at the same location.
Vault management via CLI is provided by the `dworshak secret vault` sub app, and is defined in the dworshak-secret package.

