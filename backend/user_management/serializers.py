from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=255)
    user_email = serializers.EmailField()
    user_password = serializers.CharField(min_length=8, write_only=True)


class LoginSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    user_password = serializers.CharField(write_only=True)
