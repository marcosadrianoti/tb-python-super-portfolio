import pytest
from django.contrib.auth.models import User
from projects.models import CertifyingInstitution, Certificate

pytestmark = pytest.mark.dependency()


@pytest.fixture(autouse=True)
def authenticate_before_tests(client):
    user = User.objects.get(id=1)
    client.force_authenticate(user)


def test_certificate_post_request(client):
    response = client.post(
        "/certificates/",
        {
            "name": "Certificate 2",
            "certifying_institution": 1,
            "profiles": [1]
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.json().keys() == {"id",
                                      "name",
                                      "certifying_institution",
                                      "timestamp",
                                      "profiles"}
    assert response.json()['id'] == 2
    assert response.json()['name'] == "Certificate 2"
    assert response.json()['certifying_institution'] == 1
    assert Certificate.objects.count() == 2


def test_certificate_post_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.post(
        "/certificates/",
        {
            "name": "Certificate 2",
            "certifying_institution": 1,
            "profiles": [1]
        },
        format="json",
    )
    assert response.status_code == 401
    assert Certificate.objects.count() == 1


def test_certificate_get_all_request(client):
    response = client.get("/certificates/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].keys() == {"id",
                                         "name",
                                         "certifying_institution",
                                         "timestamp",
                                         "profiles"}
    assert response.json()[0]['id'] == 1
    assert response.json()[0]['name'] == "Certificate 1"
    assert response.json()[0]['certifying_institution'] == 1


def test_certificate_get_all_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.get("/certificates/")
    assert response.status_code == 401


def test_certificate_get_one_request(client):
    response = client.get("/certificates/1/")

    assert response.status_code == 200
    assert response.json().keys() == {"id",
                                      "name",
                                      "certifying_institution",
                                      "timestamp",
                                      "profiles"}
    assert response.json()['id'] == 1
    assert response.json()['name'] == "Certificate 1"
    assert response.json()['certifying_institution'] == 1


def test_certificate_get_one_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.get("/certificates/1/")
    assert response.status_code == 401


def test_certificate_patch_request(client):
    response = client.patch(
        "/certificates/1/",
        {
            "name": "Certificate 2",
        },
        format="json",
    )

    assert response.status_code == 200
    assert Certificate.objects.count() == 1
    assert Certificate.objects.get().name == "Certificate 2"


def test_certificate_patch_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.patch(
        "/certificates/1/",
        {
            "name": "Certificate 2",
        },
        format="json",
    )
    assert response.status_code == 401
    assert Certificate.objects.count() == 1
    assert Certificate.objects.get().name == "Certificate 1"


def test_certificate_delete_request(client):
    response = client.delete("/certificates/1/")
    assert response.status_code == 204
    assert Certificate.objects.count() == 0


def test_certificate_delete_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.delete("/certificates/1/")
    assert response.status_code == 401
    assert Certificate.objects.count() == 1


def test_certifying_institution_post_request(client):
    response = client.post(
        "/certifying-institutions/",
        {
            "name": "Certifying Institution 2",
            "url": "http://myfakeurl.com",
            "certificates": [
                {
                    "name": "Certificate 2"
                }
            ]
        },
        format="json",
    )

    assert response.status_code == 201

    response_json = response.json()
    assert response.json().keys() == {"id",
                                      "name",
                                      "url",
                                      "certificates"}
    assert response_json['id'] == 2
    assert response_json['name'] == "Certifying Institution 2"
    assert response_json['url'] == "http://myfakeurl.com"
    assert response_json['certificates'][0]['name'] == "Certificate 2"
    assert CertifyingInstitution.objects.count() == 2
    assert Certificate.objects.count() == 2


def test_certifying_institution_get_all_request(client):
    response = client.get("/certifying-institutions/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].keys() == {"id",
                                         "name",
                                         "url",
                                         "certificates"}
    assert response.json()[0]['id'] == 1
    assert response.json()[0]['name'] == "Certifying Institution 1"
    assert response.json()[0]['url'] == "http://myfakeurl.com"
    assert response.json()[0]['certificates'][0]['name'] == "Certificate 1"


def test_certifying_institution_get_one_request(client):
    response = client.get("/certifying-institutions/1/")

    assert response.status_code == 200
    assert response.json().keys() == {"id",
                                      "name",
                                      "url",
                                      "certificates"}
    assert response.json()['id'] == 1
    assert response.json()['name'] == "Certifying Institution 1"
    assert response.json()['url'] == "http://myfakeurl.com"
    assert response.json()['certificates'][0]['name'] == "Certificate 1"


def test_certifying_institution_patch_request(client):
    response = client.patch(
        "/certifying-institutions/1/",
        {
            "name": "Certifying Institution 2",
            "url": "http://myfakeurl.com",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.json().keys() == {"id",
                                      "name",
                                      "url",
                                      "certificates"}
    assert response.json()['id'] == 1
    assert response.json()['name'] == "Certifying Institution 2"
    assert response.json()['url'] == "http://myfakeurl.com"
    assert CertifyingInstitution.objects.count() == 1
    assert Certificate.objects.count() == 1


def test_certifying_institution_delete_request(client):
    response = client.delete("/certifying-institutions/1/")
    assert response.status_code == 204
    assert CertifyingInstitution.objects.count() == 0
    assert Certificate.objects.count() == 0


def test_certifying_institution_post_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.post(
        "/certifying-institutions/",
        {
            "name": "Certifying Institution 2",
            "url": "http://myfakeurl.com",
            "certificates": [
                {
                    "name": "Certificate 2"
                }
            ]
        },
        format="json",
    )

    assert response.status_code == 401
    assert CertifyingInstitution.objects.count() == 1
    assert Certificate.objects.count() == 1


def test_certifying_institution_get_all_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.get("/certifying-institutions/")
    assert response.status_code == 401


def test_certifying_institution_get_one_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.get("/certifying-institutions/1/")
    assert response.status_code == 401


def test_certifying_institution_patch_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.patch(
        "/certifying-institutions/1/",
        {
            "name": "Certifying Institution 2",
            "url": "http://myfakeurl.com",
        },
        format="json",
    )
    assert response.status_code == 401
    assert CertifyingInstitution.objects.count() == 1
    assert CertifyingInstitution.objects.get().name == \
           "Certifying Institution 1"
    assert Certificate.objects.count() == 1


def test_certifying_institution_delete_request_without_authentication(client):
    client.force_authenticate(user=None)
    response = client.delete("/certifying-institutions/1/")
    assert response.status_code == 401
    assert CertifyingInstitution.objects.count() == 1
    assert Certificate.objects.count() == 1


@pytest.mark.dependency(
    depends=[
        "test_certificate_post_request",
        "test_certificate_get_all_request",
        "test_certificate_get_one_request",
        "test_certificate_patch_request",
        "test_certificate_delete_request",
        "test_certificate_post_request_without_authentication",
        "test_certificate_get_all_request_without_authentication",
        "test_certificate_get_one_request_without_authentication",
        "test_certificate_patch_request_without_authentication",
        "test_certificate_delete_request_without_authentication",
        "test_certifying_institution_post_request",
        "test_certifying_institution_get_all_request",
        "test_certifying_institution_get_one_request",
        "test_certifying_institution_patch_request",
        "test_certifying_institution_delete_request",
    ]
)
def test_validate_certificate_and_certifying_institutions_crud():
    pass
