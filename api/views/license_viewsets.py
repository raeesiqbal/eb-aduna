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
from license.models import *

# serializers
from api.serializers.create_serializers import SessionCreateSerializer
from api.serializers.get_serializers import SessionLogoutSerializer


class LicenseViewSet(BaseViewset):
    """
    API endpoints that manages licenses
    """

    action_serializers = {
        "session": SessionCreateSerializer,
        "session_logout": SessionLogoutSerializer,
    }

    action_permissions = {
        "default": [IsAuthenticated, IsSuperAdmin],
        "session": [IsAuthenticated],
        "session_logout": [IsAuthenticated],
    }

    @action(detail=False, url_path="session", methods=["post"])
    def session(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_name = serializer.validated_data["product_name"]
        machine_name = serializer.validated_data["machine_name"]
        product = Product.objects.filter(name__iexact=product_name).first()
        if not product:
            return Response(
                {
                    "status": "error",
                    "message": f'Product "{product_name}" does not exists',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        product_license = License.objects.filter(
            user=request.user, product_version__product=product
        ).first()
        if not product_license:
            return Response(
                {
                    "status": "error",
                    "message": f'License for product "{product.name}" does not exists for the user "{request.user.email}"',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        session = Session.objects.filter(
            license=product_license, machine_name=machine_name, is_active=True
        ).first()
        if session:
            return Response(
                {"status": "success", "message": "Session already exists and active"},
                status=status.HTTP_200_OK,
            )
        active_sessions = Session.objects.filter(
            license=product_license, is_active=True
        )
        if active_sessions.count() >= product_license.machines_allowed:
            machine_names = active_sessions.values_list("machine_name", flat=True)
            machine_names_list = list(machine_names)
            machine_names_str = ", ".join(machine_names_list)
            return Response(
                {
                    "status": "error",
                    "message": f'No more floating licence avaiable, current user list "{machine_names_str}"',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        Session.objects.create(
            license=product_license, machine_name=machine_name, is_active=True
        )
        return Response(
            {"status": "success", "message": "Session is created"},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, url_path="session-logout", methods=["post"])
    def session_logout(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        machine_name = serializer.validated_data["machine_name"]
        if Session.objects.filter(machine_name=machine_name, is_active=True).exists():
            active_sessions = Session.objects.filter(
                machine_name=machine_name, is_active=True
            )
            for session in active_sessions:
                session.is_active = False
                session.end_time = datetime.datetime.now()
                session.save()
            return Response(
                {
                    "status": "success",
                    "message": f'Machine "{machine_name}" is logout successfully from the sessions',
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": "error",
                "message": f'There are no active sessions for the machine "{machine_name}" to logout',
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
