from django.contrib import admin

from projects.models import (
    Profile,
    Project,
    CertifyingInstitution,
    Certificate,
)


class CertificateInline(admin.StackedInline):
    model = Certificate


class CertifyingInstitutionAdmin(admin.ModelAdmin):
    inlines = [CertificateInline]


admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(CertifyingInstitution, CertifyingInstitutionAdmin)
admin.site.register(Certificate)
