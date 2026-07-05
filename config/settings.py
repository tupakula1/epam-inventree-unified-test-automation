"""Global settings loader using .env and config/environments.yml."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
ENVIRONMENTS_FILE = PROJECT_ROOT / "config" / "environments.yml"

load_dotenv(dotenv_path=ENV_FILE)


def _as_bool(value: str | bool | None, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _load_environment_profiles() -> dict[str, dict[str, Any]]:
    if not ENVIRONMENTS_FILE.exists():
        return {}

    with ENVIRONMENTS_FILE.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream) or {}

    return data if isinstance(data, dict) else {}


class Settings:
    def __init__(self) -> None:
        profiles = _load_environment_profiles()

        self.ENV = os.getenv("ENV", "local")
        profile = profiles.get(self.ENV, {})

        self.UI_BASE_URL = (
            os.getenv("UI_BASE_URL")
            or os.getenv("BASE_URL")
            or profile.get("ui_base_url")
            or profile.get("base_url", "https://demo.inventree.org")
        )
        self.API_BASE_URL = os.getenv("API_BASE_URL") or profile.get("api_base_url", "https://demo.inventree.org/api")

        # Backward-compatible alias used by a few legacy modules.
        self.BASE_URL = self.UI_BASE_URL

        self.DOCS_UI_URL = os.getenv("DOCS_UI_URL", "https://docs.inventree.org/en/stable/part/")
        self.DOCS_API_URL = os.getenv("DOCS_API_URL", "https://docs.inventree.org/en/stable/api/schema/part/")

        self.USERNAME = os.getenv("INVENTREE_USERNAME", "admin")
        self.PASSWORD = os.getenv("INVENTREE_PASSWORD", "inventree")

        self.BROWSER = os.getenv("BROWSER") or profile.get("browser", "chromium")
        self.HEADLESS = _as_bool(os.getenv("HEADLESS"), default=_as_bool(profile.get("headless"), default=False))
        self.SLOW_MO = int(os.getenv("SLOW_MO", "0"))

        self.DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
        self.NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "60000"))


settings = Settings()
