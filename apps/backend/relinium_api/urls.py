from __future__ import annotations

from django.http import JsonResponse
from django.urls import path

from cockpit import views

try:
    from strawberry.django.views import GraphQLView

    from relinium_api.schema import schema
except ImportError:
    GraphQLView = None
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
    path("api/ssot/summary", views.ssot_summary),
    path("api/events/streams", views.event_streams),
    path("api/events", views.events),
    path("api/validation/status", views.validation_status),
    path("api/validation/known-findings", views.known_findings),
    path("graphql", GraphQLView.as_view(schema=schema) if GraphQLView else graphql_unavailable),
]
