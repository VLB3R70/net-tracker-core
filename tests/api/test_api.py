import pytest
from flask import json

import nettrackercore.api.app as flask_app


@pytest.fixture
def app():
    flask_app.app.config.update({"TESTING": True})
    return flask_app.app


@pytest.fixture
def client(app):
    return app.test_client()


def test_redirect_to_networks(client):
    url = "/"

    response = client.get(url)

    assert response.status_code == 302


def test_get_networks(client):
    url = "/networks"

    response = client.get(url)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, list)


def test_get_network(client):
    url = "/networks/redCasa"

    response = client.get(url)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert response.headers.get('Content-Type') == 'application/json'
    assert isinstance(data, dict)
    assert isinstance(data["subnet_mask"], int) and data["subnet_mask"] >= 0
    assert isinstance(data["gateway"], dict)
