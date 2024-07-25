# Imports
from rest_framework.routers import DefaultRouter
from api.views.user_viewsets import UserViewSet
from api.views.license_viewsets import LicenseViewSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("license", LicenseViewSet, basename="license")


app_name = "api"

urlpatterns = []

urlpatterns = urlpatterns + router.urls
