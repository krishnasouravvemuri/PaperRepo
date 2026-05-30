"""Cookie-JWT auth middleware. Injects request.META['user_id'] on valid token."""

from django.conf import settings
from django.http import JsonResponse

from src.utils.jwt_code import decode_jwt_token

EXEMPT_PATHS: tuple[str, ...] = (
    "/api/v2/user_management/signup",
    "/api/v2/user_management/login",
)

# Public read access (browse without login). Writes still require auth.
PUBLIC_GET_PREFIXES: tuple[str, ...] = (
    "/api/v2/question_paper_management",
    "/api/v2/important_topic_management",
    "/api/v2/material_management",
    "/api/v2/subject_management",
)


def _reject(message: str, code: int) -> JsonResponse:
    return JsonResponse(
        {"meta": {"code": code, "message": message}, "data": None},
        status=code,
    )


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith(EXEMPT_PATHS):
            return self.get_response(request)

        token = request.COOKIES.get(settings.AUTH_COOKIE_NAME)

        is_public_get = request.method in ("GET", "HEAD") and path.startswith(PUBLIC_GET_PREFIXES)
        # "My uploads" listings need auth even on GET; file-serve stays public.
        if "/my_uploads" in path:
            is_public_get = False

        if not token:
            if is_public_get:
                request.META["user_id"] = None
                return self.get_response(request)
            return _reject("Please login!", 401)

        success, message, payload = decode_jwt_token(token=token)
        if not success:
            if is_public_get:
                request.META["user_id"] = None
                return self.get_response(request)
            return _reject(message or "Invalid or expired token.", 401)

        request.META["user_id"] = payload.get("user_id")
        request.META["user_email"] = payload.get("user_email")
        request.META["user_name"] = payload.get("user_name")
        return self.get_response(request)
