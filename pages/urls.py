# Imports
from django.urls import path
from .views import *

urlpatterns = [
    path("", LendingView.as_view(), name="lending"),
    path("home", HomeView.as_view(), name="home"),
    path("contact", ContactView.as_view(), name="contact"),
    path("studio", StudioView.as_view(), name="studio"),
    path("terms", TermsView.as_view(), name="terms"),
    path("privacy-policy", PrivacyPolicyView.as_view(), name="privacy_policy"),
]
