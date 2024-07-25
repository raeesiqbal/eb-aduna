from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import DateTimeField
from django.utils import timezone

# Create your models here.


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    icon = models.ImageField(_("Icon"))
    related_software_name = models.CharField(
        _("Related Software Name"), max_length=50, null=True, blank=True
    )
    related_software_icon = models.ImageField(
        _("Related Software Icon"), null=True, blank=True
    )
    short_description = models.TextField(_("Short Description"))
    long_description = models.TextField(_("Long Description"))
    image_1 = models.ImageField(_("Image 1"), null=True, blank=True)
    image_2 = models.ImageField(_("Image 2"), null=True, blank=True)
    embed_video = models.TextField(_("Embed Video"), null=True, blank=True)
    display_order = models.IntegerField(_("Display Ordr"), null=True, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductVersion(models.Model):
    product = models.ForeignKey(
        "license.Product",
        verbose_name=_("Product"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="product_versions",
    )
    version_name = models.CharField(_("Version Name"), max_length=250)
    download_link = models.URLField(
        _("Download Link"), max_length=200, null=True, blank=True
    )
    release_date = models.DateField(
        _("Release Date"), auto_now=False, auto_now_add=False
    )
    is_latest = models.BooleanField(_("Latest Version"), default=False)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.version_name}"

    class Meta:
        verbose_name = "Product Version"
        verbose_name_plural = "Product Versions"


class ProductAction(models.Model):
    product = models.ForeignKey(
        "license.Product",
        verbose_name=_("Product"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="product_actions",
    )
    name = models.CharField(_("Name"), max_length=250)
    cost = models.FloatField(_("Cost"), null=True, blank=True)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Product Action"
        verbose_name_plural = "Product Actions"


class License(models.Model):
    LICENSE_STATUS = (
        (("active"), "Active"),
        (("cancelled"), "Cancelled"),
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name=_("User"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_licenses",
    )
    product_version = models.ForeignKey(
        "license.ProductVersion",
        verbose_name=_("Product Version"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="product_version_licenses",
    )
    status = models.CharField(
        _("License Status"), choices=LICENSE_STATUS, default="active", max_length=50
    )
    machines_allowed = models.IntegerField(_("Machines Allowed"), default=1)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user_name} --> {self.product_version.product.name}"

    class Meta:
        verbose_name = "License"
        verbose_name_plural = "Licenses"


class Session(models.Model):
    license = models.ForeignKey(
        "license.License",
        verbose_name=_("License"),
        on_delete=models.CASCADE,
        related_name="license_sessions",
    )
    machine_name = models.CharField(_("Machine Name"), max_length=50)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"{self.license__user__email} --> {self.license.product_version.product.name}"

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"


class ProductActionCount(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name=_("User"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_action_counts",
    )
    product_action = models.ForeignKey(
        "license.ProductAction",
        verbose_name=_("Product Action"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="product_action_counts",
    )
    count = models.IntegerField(_("Count"), default=1)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_action.name} --> {self.count}"

    class Meta:
        verbose_name = "Product Action Count"
        verbose_name_plural = "Product Action Counts"
