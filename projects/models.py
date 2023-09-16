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


class Project(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(
        null=False,
        blank=False,
        validators=[MaxLengthValidator(limit_value=500)],
    )
    github_url = models.URLField(null=False, blank=False)
    keyword = models.CharField(max_length=50, null=False, blank=False)
    key_skill = models.CharField(max_length=50, null=False, blank=False)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='projects'
    )

    def __str__(self):
        return self.name


class CertifyingInstitution(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    url = models.URLField(null=False, blank=False)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    certifying_institution = models.ForeignKey(
        CertifyingInstitution,
        on_delete=models.CASCADE,
        related_name="certificates",
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    profiles = models.ManyToManyField("Profile", related_name="certificates")

    def __str__(self):
        return self.name
