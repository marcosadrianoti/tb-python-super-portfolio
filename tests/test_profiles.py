import pytest
from django.contrib.auth.models import User
from projects.models import Profile
from pytest_django.asserts import assertTemplateUsed, assertContains

pytestmark = pytest.mark.dependency()


@pytest.fixture(autouse=True)
def authenticate_before_tests(client):
    user = User.objects.get(id=1)
    client.force_authenticate(user)


def test_profile_post_request(client):
    response = client.post(
        "/profiles/",
        {
            "name": "Profile 2",
            "github": "http://myfakeurl.com",
            "linkedin": "http://myfakeurl.com",
            "bio": "Bio do profile 2",
        },
        format="json",
    )
    assert response.status_code == 201
    assert Profile.objects.count() == 2
    assert Profile.objects.get(id=2).name == "Profile 2"


def test_profile_post_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.post(
        "/profiles/",
        {
            "name": "Profile 2",
            "github": "http://myfakeurl.com",
            "linkedin": "http://myfakeurl.com",
            "bio": "Bio do profile 2",
        },
        format="json",
    )
    assert response.status_code == 401
    assert Profile.objects.count() == 1


def test_profile_get_all_request(client):
    response = client.get("/profiles/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Profile 1",
            "github": "http://myfakeurl.com",
            "linkedin": "http://myfakeurl.com",
            "bio": "Bio do profile 1",
        }
    ]


def test_profile_patch_request(client):
    response = client.patch(
        "/profiles/1/",
        {
            "name": "Profile 2",
            "github": "http://myfakeurl.com",
            "linkedin": "http://myfakeurl.com",
            "bio": "Bio do profile 2",
        },
        format="json",
    )
    assert response.status_code == 200
    assert Profile.objects.count() == 1
    assert Profile.objects.get().name == "Profile 2"
    assert Profile.objects.get().bio == "Bio do profile 2"


def test_profile_patch_request_without_authentication(client):
    client.force_authenticate(user=None)

    response = client.patch(
        "/profiles/1/",
        {
            "name": "Profile 2",
            "github": "http://myfakeurl.com",
            "linkedin": "http://myfakeurl.com",
            "bio": "Bio do profile 2",
        },
        format="json",
    )
    assert response.status_code == 401
    assert Profile.objects.count() == 1
    assert Profile.objects.get().name == "Profile 1"
    assert Profile.objects.get().bio == "Bio do profile 1"


def test_profile_delete_request(client):
    response = client.delete("/profiles/1/")
    assert response.status_code == 204
    assert Profile.objects.count() == 0


def test_profile_delete_request_without_authentication(client):
    client.force_authenticate(user=None)

    response = client.delete("/profiles/1/")
    assert response.status_code == 401
    assert Profile.objects.count() == 1


def test_profile_template_without_authentication(client):
    client.force_authenticate(user=None)

    response = client.get("/profiles/1/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profile_detail.html")
    assertContains(response, "Profile 1")
    assertContains(response, "Bio do profile 1")


def test_complete_profile_template_without_authentication(client):
    response = client.get("/profiles/1/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profile_detail.html")
    assertContains(response, "Profile 1")
    assertContains(response, "Bio do profile 1")
    assertContains(response, "Projeto 1")
    assertContains(response, "keyword1")
    assertContains(response, "key_skill1")
    assertContains(response, "Certificate 1")
    assertContains(response, "Certifying Institution 1")


@pytest.mark.dependency(
    depends=[
        "test_profile_post_request",
        "test_profile_get_all_request",
        "test_profile_patch_request",
        "test_profile_delete_request",
    ]
)
def test_validate_profiles_crud():
    pass


@pytest.mark.dependency(
    depends=[
        "test_profile_template_without_authentication",
    ]
)
def test_validate_profiles_template():
    pass


@pytest.mark.dependency(
    depends=[
        "test_profile_template_without_authentication",
        "test_complete_profile_template_without_authentication",
    ]
)
def test_validate_complete_profiles_template():
    pass
