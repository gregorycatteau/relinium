from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE_DIR.parents[1]
SSOT_ROOT = REPO_ROOT / "ssot-root"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "relinium-local-cockpit-dev-only")
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in {"1", "true", "yes", "on"}
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
ROOT_URLCONF = "relinium_api.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "cockpit",
    "ssot_validation",
    "ssot_index",
    "jobs",
    "auditlog",
    "scam_trace",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "cockpit.middleware.LocalCorsMiddleware",
]

USE_TZ = True
TIME_ZONE = "UTC"


def build_postgres_database(url: str) -> dict[str, object]:
    parsed = urlparse(url)
    if parsed.scheme not in {"postgres", "postgresql"}:
        raise ImproperlyConfigured("DATABASE_URL must use the postgresql:// scheme. SQLite is not supported.")
    if not parsed.hostname or not parsed.path or parsed.path == "/":
        raise ImproperlyConfigured("DATABASE_URL must include host and database name.")

    query = parse_qs(parsed.query)
    options = {}
    if "sslmode" in query and query["sslmode"]:
        options["sslmode"] = query["sslmode"][0]

    config: dict[str, object] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": unquote(parsed.path.lstrip("/")),
        "USER": unquote(parsed.username or ""),
        "PASSWORD": unquote(parsed.password or ""),
        "HOST": parsed.hostname,
        "PORT": str(parsed.port or 5432),
    }
    if options:
        config["OPTIONS"] = options
    return config


DATABASE_URL = os.environ.get("DATABASE_URL")
RELINIUM_DATABASE_MODE = os.environ.get("RELINIUM_DATABASE_MODE", "db" if DATABASE_URL else "readonly")

if RELINIUM_DATABASE_MODE not in {"db", "readonly"}:
    raise ImproperlyConfigured("RELINIUM_DATABASE_MODE must be either 'db' or 'readonly'.")

if RELINIUM_DATABASE_MODE == "db" and not DATABASE_URL:
    raise ImproperlyConfigured("DATABASE_URL is required when RELINIUM_DATABASE_MODE=db. SQLite is not supported.")

DATABASES = {"default": build_postgres_database(DATABASE_URL)} if DATABASE_URL else {}
