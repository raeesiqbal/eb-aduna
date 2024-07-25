# Imports
from django.urls import path
from .views import *

urlpatterns = [
    path("newsletter", NewsLetterView.as_view(), name="newsletter"),
]
