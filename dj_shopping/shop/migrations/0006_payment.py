# Generated by Django 4.2 on 2023-05-05 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_alter_brand_name_alter_category_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                    "transaction_id",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("date", models.DateTimeField(auto_now=True)),
                ("pay_method", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "customer_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("card_num", models.IntegerField(blank=True, null=True)),
                ("expiry", models.IntegerField(blank=True, null=True)),
                ("cvv", models.IntegerField(blank=True, null=True)),
                ("bank_name", models.CharField(blank=True, max_length=100, null=True)),
                ("branch", models.CharField(blank=True, max_length=100, null=True)),
                ("account_num", models.IntegerField(blank=True, null=True)),
                ("ifsc", models.IntegerField(blank=True, null=True)),
                ("amount", models.FloatField(blank=True, null=True)),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="shop.order",
                    ),
                ),
            ],
        ),
    ]
