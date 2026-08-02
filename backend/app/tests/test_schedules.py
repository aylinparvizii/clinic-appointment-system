def test_doctor_schedule(test_client):

    response = test_client.get(
        "/schedules/doctor/1"
    )


    assert response.status_code == 200


    assert isinstance(
        response.json(),
        list
    )



def test_my_schedule(
    test_client,
    doctor_token
):

    response = test_client.get(
        "/schedules/my",
        headers={
            "Authorization":
            f"Bearer {doctor_token}"
        }
    )


    assert response.status_code == 200