# Project Dworshak 🌊

**Dworshak** is a high-integrity orchestration engine designed to manage the flow of infrastructure data between legacy SOAP services (EDS) and modern REST APIs (RJN). Like its namesake dam, it provides a stable, controlled interface for a high-pressure environment.

## 🏗 The Ultimate Vision
To become the definitive **single-point-of-truth orchestration layer** for regional water/infrastructure data. 
* **The Goal:** A system where data is fetched, validated, and mirrored locally so that decision-support tools (Dashboards, Alarms) never have to "wait" on a slow external API.
* **The Method:** "Do one boring thing well." Dworshak doesn't try to *be* the dashboard; it provides the *clean water* (data) that the dashboard drinks.

## ⚖️ User Stories
Dworshak supports two complementary roles within the infrastructure data ecosystem:
1. Infrastructure Integrator (Primary User)
> I need a secure, predictable tool that orchestrates the movement of data between upstream and downstream systems — pulling from legacy SOAP endpoints, transforming or validating as needed, and pushing clean, trusted data to the services that depend on it.
> Dworshak should behave like a controlled “data dam,” ensuring one‑directional flow, consistent execution across platforms, and strict protection of credentials.
2. Data Analyst (Secondary User)
> I need a reliable, set-and-forget tool that synchronizes remote API data into a local, high-performance SQLite mirror, so that dashboards, reports, and decision-support tools never have to wait on slow or unreliable external services. Equipped with the Dworshak CLI and the wider Dworshak microsuite, I can build visualizations and reports without worrying about credential leaks, API timeouts, or platform-specific (Windows vs. Termux) bugs.

## 🚀 The MVP (Current State)
- **Secure Vault:** Fernet-encrypted SQLite storage for API credentials.
- **Root of Trust:** A local `.key` file architecture that works identically on Windows and Termux.
- **CLI Entry:** A `typer`-based interface for setup and credential management.

## ⚠️ Risks & Guardrails
To prevent "going off the rails" or drowning in scope creep:
1. **The "Read-Only" UI Rule:** The web dashboard must NEVER have write-access to the APIs. Dworshak is a one-way dam, not a two-way bridge.
2. **No "Feature Bloat":** If a feature doesn't help move data from Point A to Point B more securely or faster, it doesn't belong in `core`.
3. **The Anti-Daemon Bias:** Stay script-based. Using `task-scheduler` or `cron` is more robust than maintaining a long-running daemon process that can leak memory or crash silently.

## 🛠 Installation & Setup

### Prerequisites
- Python 3.12+
- `uv` (Recommended package manager)

### Quick Start
```bash
# Initialize the project
uv sync

# Bootstrap the security layer
uv run python src/dworshak/cli.py setup

# Register your first API
uv run python src/dworshak/cli.py register --service rjn_api --item primary
```
