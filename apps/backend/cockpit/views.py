from __future__ import annotations

from django.http import JsonResponse

from cockpit import services


def api_response(data, status=200):
    return JsonResponse(data, status=status, json_dumps_params={"indent": 2})


def health(request):
    return api_response({"status": "ok", **services.json_response_data()})


def ssot_summary(request):
    return api_response(services.collect_summary())


def event_streams(request):
    return api_response({"streams": services.collect_streams()})


def events(request):
    data = services.collect_events()
    data["documents"] = services.collect_documents()["documents"]
    return api_response(data)


def validation_status(request):
    return api_response(services.collect_validation())


def known_findings(request):
    return api_response(services.load_known_findings())
