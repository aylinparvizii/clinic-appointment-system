def test_doctor_reviews(test_client):

    response = test_client.get(
        "/reviews/doctor/1"
    )


    assert response.status_code == 200


    assert isinstance(
        response.json(),
        list
    )

def test_create_review(
    test_client,
    patient_token
):

    response = test_client.post(
        "/reviews/",
        headers={
            "Authorization":
            f"Bearer {patient_token}"
        },
        json={
            "doctor_id":1,
            "rating":5,
            "comment":"good"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200