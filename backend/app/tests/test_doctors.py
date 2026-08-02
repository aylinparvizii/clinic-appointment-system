from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_get_doctors(test_client):

    response = test_client.get(
        "/doctors/"
    )


    assert response.status_code == 200


    assert isinstance(
        response.json(),
        list
    )