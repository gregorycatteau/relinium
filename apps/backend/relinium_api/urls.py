from __future__ import annotations

from django.urls import path

from cockpit import views


urlpatterns = [
    path("api/health", views.health),
    path("api/ssot/summary", views.ssot_summary),
    path("api/events/streams", views.event_streams),
    path("api/events", views.events),
    path("api/validation/status", views.validation_status),
    path("api/validation/known-findings", views.known_findings),
]
