# Generated by Django 5.1.4 on 2025-01-16 15:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("book", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrowing",
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
                ("borrow_date", models.DateField()),
                ("expected_return_date", models.DateField()),
                ("actual_return_date", models.DateField(blank=True, null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="borrowings",
                        to="book.book",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="borrowings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
