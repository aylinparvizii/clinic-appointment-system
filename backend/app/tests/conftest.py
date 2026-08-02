import pytest
from fastapi.testclient import TestClient
from app.main import app



@pytest.fixture
def test_client():

    return TestClient(app)



@pytest.fixture
def patient_token(test_client):

    response = test_client.post(
        "/auth/login",
        json={
            "mobile":"09130000001",
            "password":"123456"
        }
    )


    assert response.status_code == 200

    return response.json()["access_token"]



@pytest.fixture
def doctor_token(test_client):

    response=test_client.post(
        "/auth/login",
        json={
            "mobile":"09120000001",
            "password":"123456"
        }
    )


    assert response.status_code==200

    return response.json()["access_token"]



@pytest.fixture
def admin_token(test_client):

    response=test_client.post(
        "/auth/login",
        json={
            "mobile":"09111111111",
            "password":"admin123"
        }
    )


    assert response.status_code==200

    return response.json()["access_token"]