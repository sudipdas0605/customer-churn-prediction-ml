"""HTTP blueprints."""

from .api import bp as api_blueprint
from .pages import bp as pages_blueprint

__all__ = ["api_blueprint", "pages_blueprint"]
