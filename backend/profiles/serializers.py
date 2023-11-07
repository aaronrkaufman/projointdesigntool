from rest_framework import serializers
from .models import Profile
from rest_framework.authtoken.models import Token


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile = Profile(
            username=validated_data["username"], email=validated_data["email"]
        )
        profile.set_password(validated_data["password"])
        profile.save()
        return profile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


# Serializer for login response
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ("key",)


class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
