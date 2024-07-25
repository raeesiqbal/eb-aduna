# Imports
from utils.serializers.base import BaseSerializer
from rest_framework import serializers

# Models
from users.models import (
    User,
)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        return data


class SessionLogoutSerializer(serializers.Serializer):
    machine_name = serializers.CharField(required=True)

    def validate(self, data):
        return data
