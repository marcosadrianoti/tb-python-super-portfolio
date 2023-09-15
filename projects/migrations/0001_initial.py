# Generated by Django 4.2.3 on 2023-09-15 14:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("name", models.CharField(max_length=100)),
                ("github", models.URLField()),
                ("linkedin", models.URLField()),
                (
                    "bio",
                    models.TextField(
                        validators=[
                            django.core.validators.MaxLengthValidator(
                                limit_value=500
                            )
                        ]
                    ),
                ),
            ],
        ),
    ]
