from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE_DIR.parents[1]
SSOT_ROOT = REPO_ROOT / "ssot-root"

SECRET_KEY = "relinium-local-cockpit-dev-only"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
ROOT_URLCONF = "relinium_api.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "cockpit",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "cockpit.middleware.LocalCorsMiddleware",
]

USE_TZ = True
TIME_ZONE = "UTC"
DATABASES = {}
