from __future__ import annotations

import json
from typing import Any

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from strawberry.django.views import GraphQLView


INTROSPECTION_DISABLED_MESSAGE = "GraphQL introspection is disabled."
REQUEST_TOO_LARGE_MESSAGE = "GraphQL request is too large."


def _json_graphql_error(message: str, status: int = 200) -> JsonResponse:
    return JsonResponse({"data": None, "errors": [{"message": message}]}, status=status)


def _contains_introspection(value: Any) -> bool:
    if isinstance(value, str):
        return "__schema" in value or "__type" in value
    if isinstance(value, list):
        return any(_contains_introspection(item) for item in value)
    if isinstance(value, dict):
        return any(_contains_introspection(item) for item in value.values())
    return False


class ReliniumGraphQLView(GraphQLView):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        max_bytes = getattr(settings, "RELINIUM_GRAPHQL_MAX_REQUEST_BYTES", 1_048_576)
        if request.method == "POST" and len(request.body) > max_bytes:
            return _json_graphql_error(REQUEST_TOO_LARGE_MESSAGE, status=413)

        if not getattr(settings, "RELINIUM_GRAPHQL_INTROSPECTION_ENABLED", False):
            if self._request_contains_introspection(request):
                return _json_graphql_error(INTROSPECTION_DISABLED_MESSAGE)

        return super().dispatch(request, *args, **kwargs)

    def _request_contains_introspection(self, request: HttpRequest) -> bool:
        if request.method == "GET":
            return _contains_introspection(request.GET)
        if request.method != "POST":
            return False
        if not request.body:
            return False
        try:
            payload = json.loads(request.body.decode(request.encoding or "utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return False
        return _contains_introspection(payload)
