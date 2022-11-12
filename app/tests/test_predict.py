import pytest
from main import app

@pytest.fixture()
def client():
    return app.test_client()

def test_predict_missing_data(client):
    resp = client.get("/predict")
    assert resp.status_code == 200
