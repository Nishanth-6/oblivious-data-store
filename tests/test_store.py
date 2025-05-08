import pytest
from backend.store import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_put_and_get(client):
    res = client.post("/put", json={"key": 5, "value": "flask-test"})
    assert res.status_code == 200

    res = client.get("/get/5")
    assert res.status_code == 200
    assert res.get_json()["value"] == "flask-test"
