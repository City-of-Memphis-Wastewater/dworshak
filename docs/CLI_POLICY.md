Below is a clean, copy-paste–ready CLI policy document tailored to the Dworshak ecosystem and the code you’ve shown.
It is written to be both developer-facing and test-enforcing.

You can put this in:

docs/cli-policy.md, or

CLI_POLICY.md at repo root, or

as a section in your main README.md



---

Dworshak CLI Policy

Version: 1.0
Applies to: dworshak, dworshak-secret, dworshak-config, dworshak-env, dworshak-prompt
Audience: CLI developers, test authors, automation users


---

1. Purpose

This document defines the behavioral contract for all Dworshak command-line interfaces.

The goals are:

Reliable bash scripting

Deterministic pytest CLI testing

Consistent human UX

Clear separation of data vs messaging

Predictable behavior across composed Typer apps


All Dworshak CLIs must follow this policy.


---

2. Core Principle (Non-Negotiable)

> STDOUT is for data.
STDERR is for humans.



This rule applies universally and without exception.


---

3. Output Channels

3.1 STDOUT (stdout)

STDOUT MUST contain only:

Machine-consumable values

Data intended for capture or piping

One value per command invocation (unless explicitly documented)


Examples:

Secret values

Env values

Prompt responses

JSON output (future)


STDOUT MUST NOT contain:

Status messages

Success messages

Rich output (tables, panels)

Explanations or context



---

3.2 STDERR (stderr)

STDERR MUST contain:

Human-readable messages

Status information

Warnings

Errors

Rich output (tables, panels, colors)


This includes:

rich.console.Console.print(...)

Confirmation prompts

Informational logging



---

4. Exit Codes

Situation	Exit Code

Successful operation	0
User cancelled / no-op	0
Expected failure (missing key, not found)	1
Invalid state (vault invalid, config corrupted)	1
Programmer error / unhandled exception	non-zero


Exit codes are part of the API contract and must be tested.


---

5. Global Flags (Required)

Every Dworshak CLI MUST implement the following flags at the root level:

5.1 --version

Prints version to STDOUT

Exits immediately with code 0

Produces no STDERR output



---

5.2 --quiet / -q

Purpose: Script-friendly mode

Behavior:

Suppresses all non-essential output

STDERR MUST be empty

STDOUT MAY contain data values

Rich output is disabled


Use cases:

Bash scripting

CI pipelines

Command substitution


Example:

PORT=$(dworshak env get PORT --quiet)


---

5.3 --verbose / -v

Purpose: Human-friendly mode

Behavior:

Enables detailed messaging

Rich output allowed

STDERR may contain explanations, context, progress


STDOUT behavior remains unchanged.


---

5.4 Flag precedence

If multiple flags are provided:

--quiet overrides --verbose


---

6. Command Output Rules

6.1 Commands that return a value

Examples:

env get

secret get --value-only

prompt ask

obtain env


Rules:

Value → STDOUT

Context → STDERR

No trailing text on STDOUT


✅ Correct:

stdout: 8080
stderr: Stored [PORT] successfully.

❌ Incorrect:

stdout: Stored [PORT] successfully. 8080


---

6.2 Commands that mutate state

Examples:

secret set

env set

vault rotate-key


Rules:

Success/failure messages → STDERR

Optional resulting value → STDOUT (if meaningful)

No duplicate messaging



---

6.3 List / Table commands

Examples:

secret list

vault health


Rules:

Human display → STDERR

No STDOUT output unless explicitly documented

Rich tables MUST be sent to STDERR



---

7. Rich Output Policy

All Rich output MUST go to STDERR.

Example:

console.print(table, stderr=True)

This ensures:

Bash pipelines remain clean

pytest stdout assertions are deterministic



---

8. Prompting & Interactivity

8.1 Prompts

Prompts MUST NOT appear in --quiet mode

Prompts MUST respect non-interactive environments

CI detection must bypass prompts safely



---

8.2 Confirmation dialogs

Default choice MUST be safe ([y/N])

Cancellation exits with code 0

Cancellation MUST NOT emit STDOUT



---

9. Error Handling

9.1 Expected errors

Examples:

Missing key

Secret not found

Config file missing


Rules:

Message → STDERR

Exit code → 1

No STDOUT output



---

9.2 Unexpected errors

Stack traces SHOULD be suppressed by default

Verbose mode MAY expose diagnostics

Exit code MUST be non-zero



---

10. Testing Contract

Every CLI command MUST be testable with:

10.1 pytest + Typer runner

Tests must assert:

Exit code

STDOUT content

STDERR content


Example:

result = runner.invoke(app, ["env", "set", "PORT", "8080", "--quiet"])

assert result.exit_code == 0
assert result.stdout.strip() == "8080"
assert result.stderr == ""


---

10.2 Subprocess (E2E)

Subprocess tests verify:

Entry point wiring

PATH resolution

Packaging behavior


They MUST NOT be the primary test mechanism.


---

11. Composition Rules (dworshak root)

The dworshak CLI:

MUST NOT reimplement subcommand logic

MUST preserve output semantics of sub-CLIs

MAY add global flags and context

MUST forward arguments transparently



---

12. Backward Compatibility

Breaking changes to:

STDOUT format

Exit codes

Flag behavior


REQUIRE a major version bump.


---

13. Summary (Golden Rules)

1. STDOUT = data


2. STDERR = humans


3. --quiet means only data


4. Rich output never goes to STDOUT


5. Exit codes are API


6. Tests enforce the contract




---

14. Compliance

All Dworshak CLI changes MUST:

Follow this policy

Include tests asserting stdout/stderr behavior

Avoid ad-hoc printing




# Dworshak CLI Policy

**Version:** 1.0  
**Applies to:** `dworshak`, `dworshak-secret`, `dworshak-config`, `dworshak-env`, `dworshak-prompt`  
**Audience:** CLI developers, test authors, automation users

---

## 1. Purpose

This document defines the **behavioral contract** for all Dworshak command-line interfaces.

The goals are:

- Reliable **bash scripting**
- Deterministic **pytest CLI testing**
- Consistent **human UX**
- Clear separation of **data vs messaging**
- Predictable behavior across composed Typer apps

All Dworshak CLIs **must** follow this policy.

---

## 2. Core Principle (Non-Negotiable)

> **STDOUT is for data.  
> STDERR is for humans.**

This rule applies universally and without exception.

---

## 3. Output Channels

### 3.1 STDOUT (`stdout`)

STDOUT **MUST** contain only:

- Machine-consumable values
- Data intended for capture or piping
- One value per command invocation (unless explicitly documented)

Examples:

- Secret values
- Env values
- Prompt responses
- JSON output (future)

STDOUT **MUST NOT** contain:

- Status messages
- Success messages
- Rich output (tables, panels)
- Explanations or context

---

### 3.2 STDERR (`stderr`)

STDERR **MUST** contain:

- Human-readable messages
- Status information
- Warnings
- Errors
- Rich output (tables, panels, colors)

This includes:

- `rich.console.Console.print(...)`
- Confirmation prompts
- Informational logging

---

## 4. Exit Codes

|Situation|Exit Code|
|---|---|
|Successful operation|`0`|
|User cancelled / no-op|`0`|
|Expected failure (missing key, not found)|`1`|
|Invalid state (vault invalid, config corrupted)|`1`|
|Programmer error / unhandled exception|non-zero|

Exit codes are **part of the API contract** and must be tested.

---

## 5. Global Flags (Required)

Every Dworshak CLI **MUST** implement the following flags at the root level:

### 5.1 `--version`

- Prints version to **STDOUT**
- Exits immediately with code `0`
- Produces no STDERR output

---

### 5.2 `--quiet / -q`

**Purpose:** Script-friendly mode

Behavior:

- Suppresses **all** non-essential output
- STDERR MUST be empty
- STDOUT MAY contain data values
- Rich output is disabled

Use cases:

- Bash scripting
- CI pipelines
- Command substitution

Example:

```bash
PORT=$(dworshak env get PORT --quiet)
```

---

### 5.3 `--verbose / -v`

**Purpose:** Human-friendly mode

Behavior:

- Enables detailed messaging
- Rich output allowed
- STDERR may contain explanations, context, progress

STDOUT behavior remains unchanged.

---

### 5.4 Flag precedence

If multiple flags are provided:

```
--quiet overrides --verbose
```

---

## 6. Command Output Rules

### 6.1 Commands that return a value

Examples:

- `env get`
- `secret get --value-only`
- `prompt ask`
- `obtain env`

Rules:

- Value → STDOUT
- Context → STDERR
- No trailing text on STDOUT

✅ Correct:

```text
stdout: 8080
stderr: Stored [PORT] successfully.
```

❌ Incorrect:

```text
stdout: Stored [PORT] successfully. 8080
```

---

### 6.2 Commands that mutate state

Examples:

- `secret set`
- `env set`
- `vault rotate-key`

Rules:

- Success/failure messages → STDERR
- Optional resulting value → STDOUT (if meaningful)
- No duplicate messaging

---

### 6.3 List / Table commands

Examples:

- `secret list`
- `vault health`

Rules:

- Human display → STDERR
- No STDOUT output unless explicitly documented
- Rich tables MUST be sent to STDERR

---

## 7. Rich Output Policy

All Rich output **MUST** go to STDERR.

Example:

```python
console.print(table, stderr=True)
```

This ensures:

- Bash pipelines remain clean
- pytest `stdout` assertions are deterministic

---

## 8. Prompting & Interactivity

### 8.1 Prompts

- Prompts MUST NOT appear in `--quiet` mode
- Prompts MUST respect non-interactive environments
- CI detection must bypass prompts safely

---

### 8.2 Confirmation dialogs

- Default choice MUST be safe (`[y/N]`)
- Cancellation exits with code `0`
- Cancellation MUST NOT emit STDOUT

---

## 9. Error Handling

### 9.1 Expected errors

Examples:

- Missing key
- Secret not found
- Config file missing

Rules:

- Message → STDERR
- Exit code → `1`
- No STDOUT output

---

### 9.2 Unexpected errors

- Stack traces SHOULD be suppressed by default
- Verbose mode MAY expose diagnostics
- Exit code MUST be non-zero

---

## 10. Testing Contract

Every CLI command MUST be testable with:

### 10.1 pytest + Typer runner

Tests must assert:

- Exit code
- STDOUT content
- STDERR content

Example:

```python
result = runner.invoke(app, ["env", "set", "PORT", "8080", "--quiet"])

assert result.exit_code == 0
assert result.stdout.strip() == "8080"
assert result.stderr == ""
```

---

### 10.2 Subprocess (E2E)

Subprocess tests verify:

- Entry point wiring
- PATH resolution
- Packaging behavior

They MUST NOT be the primary test mechanism.

---

## 11. Composition Rules (dworshak root)

The `dworshak` CLI:

- MUST NOT reimplement subcommand logic
- MUST preserve output semantics of sub-CLIs
- MAY add global flags and context
- MUST forward arguments transparently

---

## 12. Backward Compatibility

Breaking changes to:

- STDOUT format
- Exit codes
- Flag behavior

**REQUIRE a major version bump**.

---

## 13. Summary (Golden Rules)

1. STDOUT = data
2. STDERR = humans
3. `--quiet` means _only_ data
4. Rich output never goes to STDOUT
5. Exit codes are API
6. Tests enforce the contract

---

## 14. Compliance

All Dworshak CLI changes MUST:

- Follow this policy
- Include tests asserting stdout/stderr behavior
- Avoid ad-hoc printing

