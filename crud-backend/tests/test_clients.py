from http import HTTPStatus

from crud_backend.schemas.clients import ClientPublic


def test_create_client(app_client):
    res = app_client.post(
        "/clients/",
        json={
            "email": "user@example.com",
            "phone": "string",
            "company": "test_company",
        },
    )

    assert res.status_code == HTTPStatus.CREATED
    assert res.json() == {
        "id": 1,
        "company": "test_company",
        "email": "user@example.com",
    }


def test_create_client_duplicate_email(app_client, client):
    res = app_client.post(
        "/clients/",
        json={
            "company": "Another Company",
            "email": client.email,
            "phone": "0987654321",
        },
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json() == {"detail": "Email already exists"}


def test_create_client_duplicate_phone(app_client, client):
    res = app_client.post(
        "/clients/",
        json={
            "company": "Another Company",
            "email": "another@example.com",
            "phone": client.phone,
        },
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json() == {"detail": "Phone already exists"}


def test_read_clients(app_client):
    res = app_client.get("/clients/")

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"clients": []}


def test_read_clients_with_client(app_client, client):
    client_schema = ClientPublic.model_validate(client).model_dump()
    res = app_client.get("/clients/")

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"clients": [client_schema]}


def test_read_client(app_client, client):
    res = app_client.get(f"/clients/{client.id}")

    assert res.json() == {
        "id": client.id,
        "email": client.email,
        "company": client.company,
    }


def test_read_client_raise_exception(app_client):
    res = app_client.get("clients/5")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Client not found"}


def test_patch_client(app_client, client):
    res = app_client.patch(
        f"/clients/{client.id}",
        json={
            "company": "Updated Company",
            "email": "updated@example.com",
            "phone": "0987654321",
        },
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {
        "id": client.id,
        "company": "Updated Company",
        "email": "updated@example.com"
    }


def test_patch_client_not_found(app_client):
    res = app_client.patch(
        "/clients/999",
        json={
            "company": "Updated Company",
            "email": "updated@example.com",
            "phone": "0987654321",
        },
    )

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Client not found"}


def test_patch_integrity_error(app_client, client):
    app_client.post(
        "/clients/",
        json={
            "company": "test_company",
            "email": "user@example.com",
            "phone": "12345",
        },
    )

    response_patch = app_client.patch(
        f"/clients/{client.id}",
        json={
            "company": "test_company",
            "email": "user@example.com",
            "phone": "12345",
        },
    )

    assert response_patch.status_code == HTTPStatus.CONFLICT
    assert response_patch.json() == {"detail": "Email or Phone already exists"}


def test_delete_client(app_client, client):
    res = app_client.delete(f"/clients/{client.id}")

    assert res.json() == {"message": "Client deleted!"}


def test_delete_client_raise_exception(app_client):
    res = app_client.delete("/clients/5")

    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json() == {"detail": "Client not found"}
