from __future__ import annotations

from django.conf import settings
from django.http import HttpResponse


class LocalCorsMiddleware:
    """Allow local Nuxt dev servers to call the local API and GraphQL."""

    ALLOWED_ORIGINS = {
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = HttpResponse() if request.method == "OPTIONS" else self.get_response(request)
        origin = request.headers.get("Origin")
        allowed_origins = getattr(settings, "RELINIUM_CORS_ALLOWED_ORIGINS", self.ALLOWED_ORIGINS)
        if origin in allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            response["Vary"] = "Origin"
            response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
            response["Access-Control-Allow-Credentials"] = "true"
        return response
