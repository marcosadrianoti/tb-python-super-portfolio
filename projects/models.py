from django.core.validators import MaxLengthValidator
from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    github = models.URLField(null=False, blank=False)
    linkedin = models.URLField(null=False, blank=False)
    bio = models.TextField(
        null=False,
        blank=False,
        validators=[MaxLengthValidator(limit_value=500)],
    )

    def __str__(self) -> str:
        return self.name
