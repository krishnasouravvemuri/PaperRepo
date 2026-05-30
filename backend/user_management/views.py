from django.conf import settings
from rest_framework.views import APIView

from src.utils.response import ApiResponse

from .models import UserManagement
from .serializers import LoginSerializer, SignupSerializer


def _set_auth_cookie(response, token: str):
    response.set_cookie(
        key=settings.AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        max_age=settings.JWT_EXPIRY_HOURS * 3600,
    )
    return response


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(serializer.errors, 400, "Validation error.").build()

        code, message, data = UserManagement.signup(serializer.validated_data)
        response = ApiResponse(data and {"user": data["user"]}, code, message).build()
        if data:
            _set_auth_cookie(response, data["token"])
        return response


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(serializer.errors, 400, "Validation error.").build()

        code, message, data = UserManagement.login(serializer.validated_data)
        response = ApiResponse(data and {"user": data["user"]}, code, message).build()
        if data:
            _set_auth_cookie(response, data["token"])
        return response


class LogoutView(APIView):
    def post(self, request):
        response = ApiResponse(None, 200, "Logged out.").build()
        response.delete_cookie(settings.AUTH_COOKIE_NAME)
        return response


class MeView(APIView):
    def get(self, request):
        user_id = request.META.get("user_id")
        if not user_id:
            return ApiResponse(None, 401, "Please login!").build()
        code, message, data = UserManagement.me(user_id=user_id)
        return ApiResponse(data, code, message).build()
