import random
def test_register(test_client):

    response = test_client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "mobile": f"0913{random.randint(1000000,9999999)}",
            "email": f"test{random.randint(1,99999)}@gmail.com",
            "password": "123456",
            "role": "patient",
            "gender": "male",
            "birth_date": "2000-01-01"
        }
    )


    assert response.status_code == 200

    data = response.json()

    assert data["mobile"].startswith("0913")
    assert data["role"] == "patient"



def test_login(test_client):

    response = test_client.post(
        "/auth/login",
        json={
            "mobile": "09111111111",
            "password": "admin123"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert "access_token" in data



def test_get_me(test_client, admin_token):

    response = test_client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data=response.json()

    assert data["role"]=="admin"