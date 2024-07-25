from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_active",
        "display_order",
        "created_at",
        "updated_at",
    )
    search_fields = [
        "id",
        "name",
        "is_active",
        "display_order",
        "created_at",
        "updated_at",
    ]


class ProductVersionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_product_name",
        "version_name",
        "download_link",
        "release_date",
        "is_latest",
        "created_at",
        "updated_at",
    )
    search_fields = [
        "id",
        "product__name",
        "version_name",
        "download_link",
        "release_date",
        "is_latest",
        "created_at",
        "updated_at",
    ]
    raw_id_fields = ("product",)

    def get_product_name(self, obj):
        if obj.product:
            product_name = reverse(
                "admin:%s_%s_change"
                % (
                    obj.product._meta.app_label,
                    obj.product._meta.model_name,
                ),
                args=[obj.product.pk],
            )
            return format_html('<a href="{}">{}</a>', product_name, obj.product.name)
        return "-"

    get_product_name.short_description = "Product"


class LicenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_user_name",
        "get_product_version",
        "status",
        "machines_allowed",
        "created_at",
        "updated_at",
    )
    search_fields = [
        "id",
        "user__user_name",
        "product_version__version_name",
        "status",
        "machines_allowed",
        "created_at",
        "updated_at",
    ]

    raw_id_fields = (
        "product_version",
        "user",
    )

    def get_user_name(self, obj):
        if obj.user:
            user = reverse(
                "admin:%s_%s_change"
                % (
                    obj.user._meta.app_label,
                    obj.user._meta.model_name,
                ),
                args=[obj.user.pk],
            )
            return format_html('<a href="{}">{}</a>', user, obj.user.user_name)
        return "-"

    def get_product_version(self, obj):
        if obj.product_version:
            product_version = reverse(
                "admin:%s_%s_change"
                % (
                    obj.product_version._meta.app_label,
                    obj.product_version._meta.model_name,
                ),
                args=[obj.product_version.pk],
            )
            return format_html(
                '<a href="{}">{}</a>', product_version, obj.product_version.version_name
            )
        return "-"

    get_user_name.short_description = "User"
    get_product_version.short_description = "Product Version"


class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_license",
        "machine_name",
        "start_time",
        "end_time",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = [
        "id",
        "license__product_version__version_name",
        "machine_name",
        "start_time",
        "end_time",
        "is_active",
        "created_at",
        "updated_at",
    ]
    raw_id_fields = ("license",)

    def get_license(self, obj):
        if obj.license:
            license = reverse(
                "admin:%s_%s_change"
                % (
                    obj.license._meta.app_label,
                    obj.license._meta.model_name,
                ),
                args=[obj.license.pk],
            )
            return format_html(
                '<a href="{}">{}</a>', license, obj.license.product_version.product.name
            )
        return "-"

    get_license.short_description = "Product Version"


class ProductActionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_product_name",
        "name",
        "cost",
        "created_at",
        "updated_at",
    )
    search_fields = [
        "id",
        "product__name",
        "name",
        "cost",
        "created_at",
        "updated_at",
    ]
    raw_id_fields = ("product",)

    def get_product_name(self, obj):
        if obj.product:
            product_name = reverse(
                "admin:%s_%s_change"
                % (
                    obj.product._meta.app_label,
                    obj.product._meta.model_name,
                ),
                args=[obj.product.pk],
            )
            return format_html('<a href="{}">{}</a>', product_name, obj.product.name)
        return "-"

    get_product_name.short_description = "Product"


class ProductActionCountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_user_name",
        "get_product_name",
        "get_product_action",
        "count",
        "created_at",
        "updated_at",
    )
    search_fields = [
        "id",
        "user__user_name",
        "product_action__product__name",
        "product_action__name",
        "count",
        "created_at",
        "updated_at",
    ]

    raw_id_fields = (
        "product_action",
        "user",
    )

    def get_user_name(self, obj):
        if obj.user:
            user = reverse(
                "admin:%s_%s_change"
                % (
                    obj.user._meta.app_label,
                    obj.user._meta.model_name,
                ),
                args=[obj.user.pk],
            )
            return format_html('<a href="{}">{}</a>', user, obj.user.user_name)
        return "-"

    def get_product_action(self, obj):
        if obj.product_action:
            product_action = reverse(
                "admin:%s_%s_change"
                % (
                    obj.product_action._meta.app_label,
                    obj.product_action._meta.model_name,
                ),
                args=[obj.product_action.pk],
            )
            return format_html(
                '<a href="{}">{}</a>', product_action, obj.product_action.name
            )
        return "-"

    def get_product_name(self, obj):
        if obj.product_action:
            product_name = reverse(
                "admin:%s_%s_change"
                % (
                    obj.product_action.product._meta.app_label,
                    obj.product_action.product._meta.model_name,
                ),
                args=[obj.product_action.product.pk],
            )
            return format_html(
                '<a href="{}">{}</a>', product_name, obj.product_action.product.name
            )
        return "-"

    get_user_name.short_description = "User"
    get_product_name.short_description = "Product"
    get_product_action.short_description = "Product Action"


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVersion, ProductVersionAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(ProductAction, ProductActionAdmin)
admin.site.register(ProductActionCount, ProductActionCountAdmin)
