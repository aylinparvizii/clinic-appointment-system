def test_doctor_visit_records(
    test_client,
    doctor_token
):

    response = test_client.get(
        "/visit-records/doctor/my",
        headers={
            "Authorization":
            f"Bearer {doctor_token}"
        }
    )


    assert response.status_code == 200
    
def test_create_visit_record(
    test_client,
    doctor_token
):

    response = test_client.post(
        "/visit-records/",
        headers={
            "Authorization":
            f"Bearer {doctor_token}"
        },
        json={
            "appointment_id":1,
            "diagnosis":"Cold",
            "prescription":"Drug A",
            "notes":"test"
        }
    )


    assert response.status_code == 200