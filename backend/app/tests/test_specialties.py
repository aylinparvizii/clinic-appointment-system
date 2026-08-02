def test_get_specialties(test_client):

    response = test_client.get(
        "/specialties/"
    )


    assert response.status_code == 200


    data = response.json()


    assert len(data) > 0