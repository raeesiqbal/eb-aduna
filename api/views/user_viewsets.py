# imports
from utils.views.base import BaseViewset, ResponseInfo
from rest_framework.response import Response
from rest_framework import status
import jwt
from rest_framework.decorators import action
import datetime
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.contrib.auth import logout

# permissions
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsSuperAdmin


# models
from users.models import *

# serializers
from api.serializers.get_serializers import LoginSerializer


class UserViewSet(BaseViewset):
    """
    API endpoints that manages users
    """

    action_serializers = {
        "default": LoginSerializer,
        "login": LoginSerializer,
    }

    action_permissions = {
        "default": [IsAuthenticated, IsSuperAdmin],
        "login": [],
        "logout": [IsAuthenticated],
    }

    @action(detail=False, url_path="logout", methods=["post"])
    def user_logout(self, request, *args, **kwargs):
        logout(request)
        return Response(
            {"status": "success", "message": "logut successfully"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, url_path="login", methods=["post"])
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            csrf_token = get_token(request)
            return Response(
                {
                    "status": "success",
                    "message": "Logged in successfully",
                    "csrf_token": csrf_token,  # Include the CSRF token in the response
                }
            )
        else:
            return Response(
                {"status": "error", "message": "Invalid credentials"}, status=400
            )
