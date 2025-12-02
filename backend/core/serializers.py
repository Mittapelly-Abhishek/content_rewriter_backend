from rest_framework import serializers
from django.contrib.auth.models import User
from .models import RewriteHistory


# -------------------------
# User Register Serializer
# -------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


# -------------------------
# Rewrite History Serializer
# -------------------------
from rest_framework import serializers
from .models import RewriteHistory
from django.contrib.auth.models import User


class RewriteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RewriteHistory
        fields = ["id", "user", "original_text", "rewritten_text", "tone", "language", "created_at"]
        read_only_fields = ["id", "created_at", "user"]
