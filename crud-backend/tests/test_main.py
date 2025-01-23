from http import HTTPStatus


def test_read_root_returns_ok_and_message(app_client):

    res = app_client.get("/")

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"message": "Hello World!"}
