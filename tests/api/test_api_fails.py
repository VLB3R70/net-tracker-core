import pytest

import nettrackercore.api.app as flask_app


@pytest.fixture
def app():
    flask_app.app.config.update({"TESTING": True})
    return flask_app.app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_network_fail(client):
    url = "/networks/test"
    response = client.get(url)
    data = response.get_json()

    assert response.status_code == 404
    assert 'error' in data


def test_get_devices_fail(client):
    url = "/networks/test/devices"
    response = client.get(url)
    data = response.get_json()

    assert response.status_code == 404
    assert 'error' in data


def test_get_device_fail(client):
    url = "/networks/redCasa/devices/192.168.1.193"
    response = client.get(url)
    data = response.get_json()

    assert response.status_code == 404
    assert 'error' in data
