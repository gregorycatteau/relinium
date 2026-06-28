from __future__ import annotations

from django.core.exceptions import PermissionDenied, ValidationError
from graphql import GraphQLError
from strawberry.types import Info

from . import permissions, services


def request_from_info(info: Info):
    context = info.context
    return getattr(context, "request", context)


def safe_graphql_error(error: Exception) -> GraphQLError:
    if isinstance(error, PermissionDenied):
        return GraphQLError(str(error) or "Permission insuffisante.")
    if isinstance(error, ValidationError):
        messages: list[str] = []
        if hasattr(error, "message_dict"):
            for field, field_messages in error.message_dict.items():
                messages.extend(f"{field}: {message}" for message in field_messages)
        else:
            messages = [str(message) for message in error.messages]
        return GraphQLError(" ".join(messages) or "Entrée invalide.")
    return GraphQLError("Opération impossible.")


def current_request_user(info: Info):
    return services.effective_user(request_from_info(info))


def require_authenticated(info: Info):
    user = current_request_user(info)
    if not getattr(user, "is_authenticated", False):
        raise safe_graphql_error(PermissionDenied("Authentification requise."))
    return user


def current_organization_or_error(info: Info):
    user = require_authenticated(info)
    organization = permissions.get_user_organization(user)
    if organization is None:
        raise safe_graphql_error(PermissionDenied("Permission insuffisante."))
    return organization


def require_permission(info: Info, permission_code: str):
    user = require_authenticated(info)
    organization = permissions.get_user_organization(user)
    try:
        permissions.require_permission(user, organization, permission_code)
    except PermissionDenied as error:
        raise safe_graphql_error(error) from None
    return user, organization
