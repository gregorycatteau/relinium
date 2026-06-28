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


def env_bool(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).lower() in {"1", "true", "yes", "on"}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "cockpit",
    "accounts",
    "ssot_validation",
    "ssot_index",
    "jobs",
    "auditlog",
    "scam_trace",
    "source_registry",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "cockpit.middleware.LocalCorsMiddleware",
]

USE_TZ = True
TIME_ZONE = "UTC"

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = env_bool("RELINIUM_SESSION_COOKIE_SECURE", os.environ.get("DJANGO_SESSION_COOKIE_SECURE", "false"))
CSRF_COOKIE_SECURE = env_bool("RELINIUM_CSRF_COOKIE_SECURE", os.environ.get("DJANGO_CSRF_COOKIE_SECURE", "false"))
RELINIUM_GRAPHQL_INTROSPECTION_ENABLED = env_bool("RELINIUM_GRAPHQL_INTROSPECTION_ENABLED", "true" if DEBUG else "false")
RELINIUM_GRAPHQL_MAX_REQUEST_BYTES = int(os.environ.get("RELINIUM_GRAPHQL_MAX_REQUEST_BYTES", "1048576"))
RELINIUM_CORS_ALLOWED_ORIGINS = {
    origin.strip()
    for origin in os.environ.get(
        "RELINIUM_CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001,http://localhost:3002,http://127.0.0.1:3002",
    ).split(",")
    if origin.strip()
}

RELINIUM_AUTH_MODE = os.environ.get("RELINIUM_AUTH_MODE", "disabled").lower()
if RELINIUM_AUTH_MODE not in {"dev", "oidc", "disabled"}:
    raise ImproperlyConfigured("RELINIUM_AUTH_MODE must be dev, oidc, or disabled.")

RELINIUM_DEV_AUTH_ENABLED = os.environ.get("RELINIUM_DEV_AUTH_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
RELINIUM_DEV_USER_EMAIL = os.environ.get("RELINIUM_DEV_USER_EMAIL", "dev@relinium.local")
RELINIUM_DEV_USER_NAME = os.environ.get("RELINIUM_DEV_USER_NAME", "Relinium Dev")
RELINIUM_DEV_USER_ROLE = os.environ.get("RELINIUM_DEV_USER_ROLE", "owner")
RELINIUM_DEFAULT_ORG = os.environ.get("RELINIUM_DEFAULT_ORG", "Relinium Local")
RELINIUM_MFA_REQUIRED_DEFAULT = env_bool("RELINIUM_MFA_REQUIRED_DEFAULT")

OIDC_PROVIDER_NAME = os.environ.get("OIDC_PROVIDER_NAME", "").strip()
OIDC_CLIENT_ID = os.environ.get("OIDC_CLIENT_ID", "").strip()
OIDC_CLIENT_SECRET = os.environ.get("OIDC_CLIENT_SECRET", "").strip()
OIDC_DISCOVERY_URL = os.environ.get("OIDC_DISCOVERY_URL", "").strip()
OIDC_REDIRECT_URI = os.environ.get("OIDC_REDIRECT_URI", "").strip()
RELINIUM_OIDC_PROVIDER_CONFIGURED = all([OIDC_PROVIDER_NAME, OIDC_CLIENT_ID, OIDC_CLIENT_SECRET, OIDC_DISCOVERY_URL, OIDC_REDIRECT_URI])


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

if RELINIUM_DATABASE_MODE == "readonly":
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
