from __future__ import annotations

from django.http import JsonResponse
from django.urls import path

from cockpit import views

try:
    from relinium_api.graphql_view import ReliniumGraphQLView
    from relinium_api.schema import schema
except ImportError:
    ReliniumGraphQLView = None
    schema = None


def graphql_unavailable(request):
    return JsonResponse(
        {
            "error": "GraphQL dependencies are not installed. Run pip install -r apps/backend/requirements.txt.",
        },
        status=503,
    )


urlpatterns = [
    path("api/health", views.health),
    path("api/csrf", views.csrf_token),
    path("api/ssot/summary", views.ssot_summary),
    path("api/events/streams", views.event_streams),
    path("api/events", views.events),
    path("api/validation/status", views.validation_status),
    path("api/validation/known-findings", views.known_findings),
    path("graphql", ReliniumGraphQLView.as_view(schema=schema) if ReliniumGraphQLView else graphql_unavailable),
]
