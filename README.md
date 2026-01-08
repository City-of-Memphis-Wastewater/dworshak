# Project Dworshak 🌊

**Dworshak** is the security bones behind API orchestration of infrastructure data between legacy SOAP services (EDS) and modern REST APIs (RJN).

## 🏗  The Ultimate Vision
To become a stable credential management tool for scripting the flow of Emerson Ovation data and related APIs, supporting multiple projects in and beyond at the Maxson Wastewater Treatment Plant.
* **The Wider Goal:** A system where data is fetched, validated, and mirrored locally so that decision-support tools (Dashboards, Alarms) never have to "wait" on a slow external API.
* **The Method:** "Do one boring thing well." Use OpenSSL to manage a local `~/.dowrshak/ directory which includes a `.key` file, a `vault.db` encrypted credential file, and a `config.json` file for controlling defaults.

## ⚖️ User Stories
Dworshak supports two complementary roles within the infrastructure data ecosystem:
1. Infrastructure Integrator (Primary User)
> I need a secure, predictable tool that orchestrates the movement of data between upstream and downstream systems — pulling from legacy SOAP endpoints, transforming or validating as needed, and pushing clean, trusted data to the services that depend on it.
> Dworshak should behave like a controlled “data dam,” ensuring one‑directional flow, consistent execution across platforms, and strict protection of credentials.
2. Data Analyst (Secondary User)
> I need a reliable, set-and-forget tool that synchronizes remote API data into a local, high-performance SQLite mirror, so that dashboards, reports, and decision-support tools never have to wait on slow or unreliable external services. Equipped with the Dworshak CLI and its companion toolset, I can build visualizations and reports without worrying about credential leaks, API timeouts, or platform-specific (Windows vs. Termux) bugs.

## 🚀 The MVP (Current State)
- **Secure Vault:** Fernet-encrypted SQLite storage for API credentials.
- **Root of Trust:** A local `.key` file architecture that works identically on Windows and Termux.
- **CLI Entry:** A `typer`-based interface for setup and credential management.

## ⚠️ Risks & Guardrails
To prevent "going off the rails" or drowning in scope creep:
 **The Anti-Daemon Bias:** Stay script-based. Using `task-scheduler` or `cron` is more robust than maintaining a long-running daemon process that can leak memory or crash silently.

### Quick Start

```bash
# Install the CLI
pipx install dworshak

# Bootstrap the security layer
dworshak setup

# Register your first API
dworshak register --service rjn_api --item username

```
