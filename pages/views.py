# Imports
from django.shortcuts import render
from django.views.generic import View


# Views
class LendingView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/lending.html")


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/home.html")


class ContactView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/contact.html")


class StudioView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/studio.html")


class TermsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/terms.html")


class PrivacyPolicyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/privacy-policy.html")
