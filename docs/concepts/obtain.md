# Obtain: Smart Retrieval with Interactive Fallback

dworshak-prompt.Obtain is a unified mechanism to retrieve configuration, secrets, or environment values. Its purpose is to make workflows reliable, consistent, and CI-safe while reducing repetitive manual input.


---

## How Obtain Works

1. Check existing storage first

- Secrets → dworshak-secret vault

- Configurations → dworshak-config JSON files

- Environment variables → .env files via dworshak-env



2. Prompt only if needed

If the requested value is missing or overwrite=True, Obtain will ask the user for input.

Input is collected using a priority-aware default interface sequence.


3. Automatic persistence

Unless forget=True, any new or updated value is saved back to the original storage (vault, config, or env file).


### Automatic Fallback (Default Behavior)

If no interface is specified, dworshak-prompt will try:

Console → GUI → Web

Unavailable interfaces are skipped automatically.


---

## Data Structures

| Class	| Purpose |
| ------ | --------|
| ObtainResult | Generic wrapper for a retrieved value |
| SecretData | Overrides status_message for secrets |
| ConfigData | Alias for ObtainResult for config values |
| EnvData | Alias for ObtainResult for environment variables |


ObtainResult contains:

- value: Optional[str] — the retrieved value

- is_new: Optional[bool] — True if stored just now, False if already known, None if user cancelled

- status_message: str — human-readable status


---

## Using Obtain in Python

```python
from dworshak_prompt import Obtain

# Initialize the manager
obtain = Obtain()

# Retrieve a secret (check vault first, prompt if missing)
secret_val = obtain.secret("my_service", "api_key")

# Retrieve a config value (check file first, prompt if missing)
config_val = obtain.config("my_service", "timeout", suggestion="30")

# Retrieve an environment value (check .env first, prompt if missing)
env_val = obtain.env("DATABASE_URL")
```

### Using Obtain with Interface Control

```
from dworshak_prompt import obtain, PromptMode

result = obtain.secret(
    "github",
    "token",
    message="Enter your GitHub API token",
    priority_interface=[PromptMode.GUI,PromptMode.CONSOLE],
    avoid_interface={PromptMode.WEB}
)

if result:
    print(result.status_message)
    token = result.value
else:
    print("User cancelled.")
```


### Interface Selection

The prompting interface can be controlled with PromptMode.

| Mode	| Behavior |
| ------ | ------- |
| PromptMode.CONSOLE	| Force terminal input |
| PromptMode.GUI	| Use a Tkinter dialog |
| PromptMode.WEB	| Launch a local browser prompt |
| None	| Automatic fallback |


### Example forcing a GUI dialog:

```python
from dworshak_prompt import obtain, PromptMode

result = obtain.config(
    "web_service",
    "timeout",
    suggestion="30",
    priority_interface=[PromptMode.GUI]
)
```

### Avoiding an Interface

You can also skip specific interfaces:

```python
result = obtain.env(
    "DATABASE_URL",
    avoid_interface={PromptMode.WEB}
)
```

This will try:

Console → GUI

but never the web interface.

---

## Arguments the Obtain functions

- service: str,
- item: str,
- message: str | None = None,
- suggestion: str | None = None,
- default: Any | None = None,
- priority_interface: list[PromptMode] | None = None,
- avoid_interface: set[PromptMode] | None = None,
- path: str | Path | None = None,
- overwrite: bool = False,
- forget: bool = False,

---

## Key Features

- Storage-aware first: never prompts unnecessarily

- Fallback interfaces: console → GUI → web

- CI-safe: non-interactive environments return defaults

- Persistent by default: stores new values automatically

Flexible: supports secrets, config files, and environment variables

