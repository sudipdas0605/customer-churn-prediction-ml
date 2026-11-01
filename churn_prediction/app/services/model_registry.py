"""Lazy, thread-safe access to the trained model artefacts."""

from __future__ import annotations

import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib

from app.errors import ModelUnavailableError

ARTEFACT_SUFFIXES = {
    "model": "_model.pkl",
    "scaler": "_scaler.pkl",
    "encoders": "_encoders.pkl",
}


@dataclass(frozen=True)
class ModelBundle:
    """The three artefacts needed to score one domain."""

    domain: str
    model: Any
    scaler: Any
    encoders: dict[str, Any]


class ModelRegistry:
    """Loads model bundles on first use and caches them in memory."""

    def __init__(self, models_dir: Path) -> None:
        self._models_dir = Path(models_dir)
        self._cache: dict[str, ModelBundle] = {}
        self._lock = threading.Lock()

    def files_for(self, domain: str) -> dict[str, Path]:
        return {
            kind: self._models_dir / f"{domain}{suffix}"
            for kind, suffix in ARTEFACT_SUFFIXES.items()
        }

    def is_available(self, domain: str) -> bool:
        return all(path.is_file() for path in self.files_for(domain).values())

    def get(self, domain: str) -> ModelBundle:
        """Return the cached bundle for *domain*, loading it if needed."""
        cached = self._cache.get(domain)
        if cached is not None:
            return cached

        with self._lock:
            cached = self._cache.get(domain)
            if cached is not None:
                return cached

            files = self.files_for(domain)
            missing = [str(path) for path in files.values() if not path.is_file()]
            if missing:
                raise ModelUnavailableError(domain)

            try:
                bundle = ModelBundle(
                    domain=domain,
                    model=joblib.load(files["model"]),
                    scaler=joblib.load(files["scaler"]),
                    encoders=joblib.load(files["encoders"]),
                )
            except Exception as exc:  # corrupted pickle / version mismatch
                raise ModelUnavailableError(domain) from exc

            self._cache[domain] = bundle
            return bundle
