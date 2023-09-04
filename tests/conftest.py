import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope="session")
def custom_django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield


@pytest.fixture(scope="session")
def user_seed(custom_django_db_setup):
    User.objects.create_user(
        username="superuser",
        password="lookathowgoodandbigisthepass",
        is_staff=True,
        is_superuser=True,
    )


try:
    from projects.models import Profile

    @pytest.fixture(scope="session")
    def profile_seed(custom_django_db_setup):
        Profile.objects.create(
            name="Profile 1",
            github="http://myfakeurl.com",
            linkedin="http://myfakeurl.com",
            bio="Bio do profile 1",
        )

except ImportError:

    @pytest.fixture(scope="session")
    def profile_seed(custom_django_db_setup):
        ...


try:
    from projects.models import Project

    @pytest.fixture(scope="session")
    def project_seed(custom_django_db_setup):
        Project.objects.create(
            name="Projeto 1",
            description="Descrição do projeto 1",
            github_url="http://myfakeurl.com",
            keyword="keyword1",
            key_skill="key_skill1",
            profile_id=1,
        )

except ImportError:

    @pytest.fixture(scope="session")
    def project_seed(custom_django_db_setup):
        ...


try:
    from projects.models import CertifyingInstitution, Certificate, Profile

    @pytest.fixture(scope="session")
    def certificate_and_institution_seed(custom_django_db_setup):
        CertifyingInstitution.objects.create(
            name="Certifying Institution 1",
            url="http://myfakeurl.com",
        )

        certificate = Certificate.objects.create(
            name="Certificate 1",
            certifying_institution=CertifyingInstitution.objects.get(id=1),
        )

        profile = Profile.objects.get(id=1)

        profile.certificates.add(certificate)

except ImportError:

    @pytest.fixture(scope="session")
    def certificate_and_institution_seed(custom_django_db_setup):
        ...


@pytest.fixture(scope="session", autouse=True)
def seed_database(
    user_seed, profile_seed, project_seed, certificate_and_institution_seed
):
    ...
