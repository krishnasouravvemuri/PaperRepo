"""User management business logic. ORM models live in core.client_model_app."""

from django.utils import timezone

from core.client_model_app.models import UserInfo
from src.utils.hashing import hash_password, verify_password
from src.utils.jwt_code import encode_jwt_token


class UserManagement:
    @staticmethod
    def signup(payload: dict) -> tuple[int, str, dict | None]:
        email = payload["user_email"].lower().strip()
        if UserInfo.objects.filter(user_email=email, user_deleted_at__isnull=True).exists():
            return 409, "Email already registered.", None

        user = UserInfo.objects.create(
            user_email=email,
            user_name=payload["user_name"],
            user_password_hash=hash_password(payload["user_password"]),
        )
        token = UserManagement._issue_token(user)
        return 201, "Signup successful.", {"token": token, "user": UserManagement._public(user)}

    @staticmethod
    def login(payload: dict) -> tuple[int, str, dict | None]:
        email = payload["user_email"].lower().strip()
        user = UserInfo.objects.filter(user_email=email, user_deleted_at__isnull=True).first()
        if not user or not verify_password(payload["user_password"], user.user_password_hash):
            return 401, "Invalid email or password.", None
        if not user.user_is_active:
            return 403, "Account disabled.", None

        user.user_last_login_at = timezone.now()
        user.save(update_fields=["user_last_login_at"])
        token = UserManagement._issue_token(user)
        return 200, "Login successful.", {"token": token, "user": UserManagement._public(user)}

    @staticmethod
    def me(user_id: str) -> tuple[int, str, dict | None]:
        user = UserInfo.objects.filter(user_id=user_id, user_deleted_at__isnull=True).first()
        if not user:
            return 404, "User not found.", None
        return 200, "OK", {"user": UserManagement._public(user)}

    @staticmethod
    def _issue_token(user: UserInfo) -> str:
        return encode_jwt_token(
            {
                "user_id": str(user.user_id),
                "user_email": user.user_email,
                "user_name": user.user_name,
            }
        )

    @staticmethod
    def _public(user: UserInfo) -> dict:
        return {
            "user_id": str(user.user_id),
            "user_email": user.user_email,
            "user_name": user.user_name,
        }
