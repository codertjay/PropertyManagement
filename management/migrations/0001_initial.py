# Generated by Django 4.2.1 on 2023-05-17 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contract",
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
                ("name", models.CharField(blank=True, max_length=250, null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contracts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Management",
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
                ("lease_id", models.CharField(max_length=250)),
                ("lease_start_date", models.DateField(blank=True, null=True)),
                ("first_day_of_term_date", models.DateField(blank=True, null=True)),
                ("last_day_of_term_date", models.DateField(blank=True, null=True)),
                ("lease_expiration_date", models.DateField(blank=True, null=True)),
                (
                    "rent_security",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "rent_security_type",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("tenant_id", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "tenant_name",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("is_company", models.BooleanField(blank=True, null=True)),
                ("option_from_date", models.DateField(blank=True, null=True)),
                (
                    "option_to_date",
                    models.CharField(blank=True, max_length=240, null=True),
                ),
                (
                    "option_type_break_purchase_renew",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "option_type_landlord_tenant_mutual",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("term", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "notice_term",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "notice_term_date",
                    models.DateField(blank=True, max_length=250, null=True),
                ),
                (
                    "notice_term_frequency",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("fund_id", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "property_id",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("unit_id", models.CharField(blank=True, max_length=250, null=True)),
                ("unit_type", models.CharField(blank=True, max_length=250, null=True)),
                ("gross_area", models.CharField(blank=True, max_length=250, null=True)),
                ("net_area", models.CharField(blank=True, max_length=250, null=True)),
                ("is_vacant", models.BooleanField(blank=True, null=True)),
                (
                    "vacancy_reason",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "income_category_rent_amount",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "income_category_service_charges_amount",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "income_category_others_amount",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "income_category_discount_amount",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "term_frequency",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "charge_frequency",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "value_added_tax",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "value_added_tax_rate",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("start_payment_schedule", models.DateField(blank=True, null=True)),
                ("end_payment_schedule", models.DateField(blank=True, null=True)),
                ("currency", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "index_series",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("index_type", models.CharField(blank=True, max_length=250, null=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                (
                    "index_frequency",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("index_date", models.DateField(blank=True, null=True)),
                (
                    "index_value",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("next_index_date", models.DateField(blank=True, null=True)),
                (
                    "next_index_value",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "contract",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="management.contract",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="managements",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]