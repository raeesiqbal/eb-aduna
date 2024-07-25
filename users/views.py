# Imports
from django.shortcuts import redirect
from django.views.generic import View
from .models import NewsLetter
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework import status


# Views


class NewsLetterView(View):
    def get(self, request, *args, **kwargs):
        return redirect("pages:home")

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        NewsLetter.objects.create(email=email)
        return redirect("pages:home")
