# Generated by Django 4.2 on 2023-04-28 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("placed_date", models.DateTimeField(auto_now_add=True)),
                ("completed_date", models.DateTimeField(auto_now=True)),
                ("complete", models.BooleanField(default=False)),
                (
                    "transaction_id",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
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
                ("name", models.CharField(max_length=256)),
                ("price", models.FloatField()),
                ("discount", models.IntegerField()),
                ("stock", models.IntegerField()),
                ("colors", models.CharField(max_length=256)),
                ("description", models.TextField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("ratings", models.CharField(max_length=10)),
                ("badge", models.CharField(max_length=20)),
                (
                    "image1",
                    models.ImageField(
                        default="product.jpg", upload_to=shop.models.get_file_path
                    ),
                ),
                (
                    "image2",
                    models.ImageField(
                        default="product.jpg", upload_to=shop.models.get_file_path
                    ),
                ),
                (
                    "image3",
                    models.ImageField(
                        default="product.jpg", upload_to=shop.models.get_file_path
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ShipAddress",
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
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, null=True, region=None
                    ),
                ),
                ("house", models.CharField(max_length=200, null=True)),
                ("street", models.CharField(max_length=100, null=True)),
                ("city", models.CharField(max_length=100, null=True)),
                ("state", models.CharField(max_length=100, null=True)),
                ("pincode", models.IntegerField(null=True)),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="shop.order",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("quantity", models.IntegerField(default=0)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="shop.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="shop.product",
                    ),
                ),
            ],
        ),
    ]
