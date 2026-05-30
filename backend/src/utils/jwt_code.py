"""JWT encode/decode helpers."""

from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings


def encode_jwt_token(payload: dict) -> str:
    data = dict(payload)
    data["exp"] = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRY_HOURS)
    data["iat"] = datetime.now(timezone.utc)
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_jwt_token(token: str) -> tuple[bool, str, dict | None]:
    """Returns (success, message, payload)."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return True, "", payload
    except jwt.ExpiredSignatureError:
        return False, "Session expired. Please login again.", None
    except jwt.InvalidTokenError:
        return False, "Invalid token.", None
