# Imports
from utils.serializers.base import BaseSerializer
from rest_framework import serializers

# Models
from license.models import Session


class SessionCreateSerializer(serializers.Serializer):
    product_name = serializers.CharField(required=True)
    machine_name = serializers.CharField(required=True)

    def validate(self, data):
        return data
