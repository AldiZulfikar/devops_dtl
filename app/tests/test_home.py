import pytest
from main import app

@pytest.fixture()
def client():
    return app.test_client()

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b"Lets Predict Source Code of Your Software!" in resp.data

def test_home_bad_http_method(client):
    resp = client.post('/')
    assert resp.status_code == 405