# Generated by Django 5.0.3 on 2024-07-11 12:30

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name")),
                ("icon", models.ImageField(upload_to="", verbose_name="Icon")),
                (
                    "related_software_name",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Related Software Name",
                    ),
                ),
                (
                    "related_software_icon",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="",
                        verbose_name="Related Software Icon",
                    ),
                ),
                (
                    "short_description",
                    models.TextField(verbose_name="Short Description"),
                ),
                ("long_description", models.TextField(verbose_name="Long Description")),
                (
                    "image_1",
                    models.ImageField(
                        blank=True, null=True, upload_to="", verbose_name="Image 1"
                    ),
                ),
                (
                    "image_2",
                    models.ImageField(
                        blank=True, null=True, upload_to="", verbose_name="Image 2"
                    ),
                ),
                (
                    "embed_video",
                    models.TextField(blank=True, null=True, verbose_name="Embed Video"),
                ),
                (
                    "display_order",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Display Ordr"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="ProductAction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Name")),
                ("cost", models.FloatField(blank=True, null=True, verbose_name="Cost")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_actions",
                        to="license.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Action",
                "verbose_name_plural": "Product Actions",
            },
        ),
        migrations.CreateModel(
            name="ProductActionCount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("count", models.IntegerField(default=1, verbose_name="Count")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "product_action",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_action_counts",
                        to="license.productaction",
                        verbose_name="Product Action",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_action_counts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Action Count",
                "verbose_name_plural": "Product Action Counts",
            },
        ),
        migrations.CreateModel(
            name="ProductVersion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "version_name",
                    models.CharField(max_length=250, verbose_name="Version Name"),
                ),
                (
                    "download_link",
                    models.URLField(
                        blank=True, null=True, verbose_name="Download Link"
                    ),
                ),
                ("release_date", models.DateField(verbose_name="Release Date")),
                (
                    "is_latest",
                    models.BooleanField(default=False, verbose_name="Latest Version"),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_versions",
                        to="license.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Version",
                "verbose_name_plural": "Product Versions",
            },
        ),
        migrations.CreateModel(
            name="License",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("cancelled", "Cancelled")],
                        default="active",
                        max_length=50,
                        verbose_name="License Status",
                    ),
                ),
                (
                    "machines_allowed",
                    models.IntegerField(default=1, verbose_name="Machines Allowed"),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_licenses",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
                (
                    "product_version",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_version_licenses",
                        to="license.productversion",
                        verbose_name="Product Version",
                    ),
                ),
            ],
            options={
                "verbose_name": "License",
                "verbose_name_plural": "Licenses",
            },
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "machine_name",
                    models.CharField(max_length=50, verbose_name="Machine Name"),
                ),
                ("start_time", models.DateTimeField(auto_now_add=True)),
                ("end_time", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "license",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="license_sessions",
                        to="license.license",
                        verbose_name="License",
                    ),
                ),
            ],
            options={
                "verbose_name": "Session",
                "verbose_name_plural": "Sessions",
            },
        ),
    ]
