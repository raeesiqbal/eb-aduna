# Imports
from django.contrib import admin
from .models import User, NewsLetter
from django.contrib.auth.admin import UserAdmin as DjanoAdmin
from django.contrib.auth.models import Group

# Register your models here.


class UserAdmin(DjanoAdmin):
    model = User
    list_display = (
        "id",
        "email",
        "is_superuser",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "user_name",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Account",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "user_name",
                ),
            },
        ),
    )
    ordering = ("email",)
    search_fields = (
        "email",
        "user_name",
    )


class NewsLetterAmin((admin.ModelAdmin)):
    model = NewsLetter
    list_display = (
        "id",
        "email",
    )


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(NewsLetter, NewsLetterAmin)
