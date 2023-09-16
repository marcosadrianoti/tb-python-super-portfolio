from django.contrib import admin

from projects.models import (
    Profile,
    Project,
    CertifyingInstitution,
    Certificate,
)

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(CertifyingInstitution)
admin.site.register(Certificate)
