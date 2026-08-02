def test_register_invalid_email(test_client):

    response=test_client.post(
        "/auth/register",
        json={
            "first_name":"Test",
            "last_name":"User",
            "mobile":"09135555555",
            "email":"wrong-email",
            "password":"123456",
            "role":"patient"
        }
    )


    assert response.status_code==422