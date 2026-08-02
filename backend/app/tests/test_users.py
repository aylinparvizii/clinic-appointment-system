def test_users_without_token(test_client):

    response = test_client.get(
        "/users/"
    )


    assert response.status_code in [
        401,
        403
    ]



def test_get_users_admin(test_client, admin_token):

    response = test_client.get(
        "/users/",
        headers={
            "Authorization":
            f"Bearer {admin_token}"
        }
    )


    assert response.status_code == 200


    assert isinstance(
        response.json(),
        list
    )