import pytest
from django.contrib.auth.models import User
from projects.models import Project

pytestmark = pytest.mark.dependency()


@pytest.fixture(autouse=True)
def authenticate_before_tests(client):
    user = User.objects.get(id=1)
    client.force_authenticate(user)


def test_project_post_request(client):
    response = client.post(
        "/projects/",
        {
            "name": "Projeto 2",
            "description": "Descrição do projeto 2",
            "github_url": "http://myfakeurl2.com",
            "keyword": "keyword1",
            "key_skill": "key_skill1",
            "profile": 1,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 2,
        "name": "Projeto 2",
        "description": "Descrição do projeto 2",
        "github_url": "http://myfakeurl2.com",
        "keyword": "keyword1",
        "key_skill": "key_skill1",
        "profile": 1,
        }
    assert Project.objects.count() == 2


def test_project_get_all_request(client):
    response = client.get("/projects/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json() == [
        {
            "id": 1,
            "name": "Projeto 1",
            "description": "Descrição do projeto 1",
            "github_url": "http://myfakeurl.com",
            "keyword": "keyword1",
            "key_skill": "key_skill1",
            "profile": 1,
        }
    ]


def test_project_get_one_request(client):
    response = client.get("/projects/1/")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Projeto 1",
        "description": "Descrição do projeto 1",
        "github_url": "http://myfakeurl.com",
        "keyword": "keyword1",
        "key_skill": "key_skill1",
        "profile": 1,
    }


def test_project_patch_request(client):
    response = client.patch(
        "/projects/1/",
        {
            "name": "Projeto 1 alterado",
            "description": "Descrição do projeto alterada",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Projeto 1 alterado",
        "description": "Descrição do projeto alterada",
        "github_url": "http://myfakeurl.com",
        "keyword": "keyword1",
        "key_skill": "key_skill1",
        "profile": 1,
    }

    assert Project.objects.count() == 1
    assert Project.objects.get(id=1).name == "Projeto 1 alterado"
    assert (
        Project.objects.get(id=1).description
        == "Descrição do projeto alterada"
    )


def test_project_delete_request(client):
    response = client.delete("/projects/1/")

    assert response.status_code == 204
    assert Project.objects.count() == 0


def test_project_post_request_without_authentication(client):
    client.force_authenticate(user=None)

    response = client.post(
        "/projects/",
        {
            "name": "Projeto 2",
            "description": "Descrição do projeto 2",
            "github_url": "http://myfakeurl2.com",
            "keyword": "keyword1",
            "key_skill": "key_skill1",
            "profile": 1,
        },
    )

    assert response.status_code == 401
    assert Project.objects.count() == 1


def test_project_get_all_request_without_authentication(client):
    client.force_authenticate(user=None)

    response = client.get("/projects/")

    assert response.status_code == 401
    assert Project.objects.count() == 1


def test_project_get_one_request_without_authentication(client):
    client.force_authenticate(user=None)

    response = client.get("/projects/1/")

    assert response.status_code == 401
    assert Project.objects.count() == 1


def test_project_patch_request_without_authentication(client):
    client.force_authenticate(user=None)

    response = client.patch(
        "/projects/1/",
        {
            "name": "Projeto 1 alterado",
            "description": "Descrição do projeto alterada",
        },
    )

    assert response.status_code == 401
    assert Project.objects.count() == 1
    assert Project.objects.get(id=1).name == "Projeto 1"
    assert (
        Project.objects.get(id=1).description
        == "Descrição do projeto 1"
    )


def test_project_delete_request_without_authentication(client):
    client.force_authenticate(user=None)

    response = client.delete("/projects/1/")

    assert response.status_code == 401
    assert Project.objects.count() == 1


@pytest.mark.dependency(
    depends=[
        "test_project_post_request",
        "test_project_get_all_request",
        "test_project_get_one_request",
        "test_project_patch_request",
        "test_project_delete_request",
        "test_project_post_request_without_authentication",
        "test_project_get_all_request_without_authentication",
        "test_project_get_one_request_without_authentication",
        "test_project_patch_request_without_authentication",
        "test_project_delete_request_without_authentication",
    ]
)
def test_validate_projects_crud():
    pass
