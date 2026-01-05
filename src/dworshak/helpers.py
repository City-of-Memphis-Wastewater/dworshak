# src/dworshak/helpers.py
import json
from dworshak.paths import CONFIG_FILE

def load_services() -> list[str]:
    if CONFIG_FILE.exists():
        data = json.loads(CONFIG_FILE.read_text())
        return data.get("services", [])
    return ["rjn_api"]

def is_valid_service(value: str) -> bool:
    return value in load_services()
