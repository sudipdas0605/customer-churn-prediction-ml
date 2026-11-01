"""Application configuration.

Every runtime setting is read from environment variables, optionally seeded
from a local ``.env`` file (see ``.env.example``). No environment-specific
value is hard-coded in the application logic.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODELS_DIR = PROJECT_ROOT / "models"
DEFAULT_LOG_DIR = PROJECT_ROOT / "data" / "logs"


def load_dotenv(path: Path | None = None) -> None:
    """Load ``KEY=VALUE`` pairs from a .env file without overriding real env vars."""
    env_file = path or PROJECT_ROOT / ".env"
    if not env_file.is_file():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None or not value.strip():
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value else default
    except ValueError:
        return default


def _as_path(value: str | None, default: Path) -> Path:
    if not value:
        return default
    path = Path(value).expanduser()
    return path if path.is_absolute() else (PROJECT_ROOT / path).resolve()


@dataclass(frozen=True)
class Config:
    """Immutable application settings."""

    secret_key: str
    debug: bool
    host: str
    port: int
    models_dir: Path
    log_dir: Path
    log_pii: bool
    max_content_length: int
    api_prefix: str = "/api/v1"

    @property
    def flask_settings(self) -> dict:
        """Settings understood directly by Flask."""
        return {
            "SECRET_KEY": self.secret_key,
            "DEBUG": self.debug,
            "MAX_CONTENT_LENGTH": self.max_content_length,
            "HOST": self.host,
            "PORT": self.port,
            "MODELS_DIR": self.models_dir,
            "LOG_DIR": self.log_dir,
            "LOG_PII": self.log_pii,
            "API_PREFIX": self.api_prefix,
        }


def load_config() -> Config:
    """Build a :class:`Config` from the current environment."""
    load_dotenv()
    return Config(
        secret_key=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        debug=_as_bool(os.environ.get("DEBUG"), default=True),
        host=os.environ.get("HOST", "127.0.0.1"),
        port=_as_int(os.environ.get("PORT"), 5000),
        models_dir=_as_path(os.environ.get("MODELS_DIR"), DEFAULT_MODELS_DIR),
        log_dir=_as_path(os.environ.get("LOG_DIR"), DEFAULT_LOG_DIR),
        log_pii=_as_bool(os.environ.get("LOG_PII"), default=False),
        max_content_length=_as_int(os.environ.get("MAX_CONTENT_LENGTH"), 1_048_576),
    )
