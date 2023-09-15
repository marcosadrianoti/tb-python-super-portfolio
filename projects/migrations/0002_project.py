# Generated by Django 4.2.3 on 2023-09-15 20:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("name", models.CharField(max_length=50)),
                (
                    "description",
                    models.TextField(
                        validators=[
                            django.core.validators.MaxLengthValidator(
                                limit_value=500
                            )
                        ]
                    ),
                ),
                ("github_url", models.URLField()),
                ("keyword", models.CharField(max_length=50)),
                ("key_skill", models.CharField(max_length=50)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to="projects.profile",
                    ),
                ),
            ],
        ),
    ]
