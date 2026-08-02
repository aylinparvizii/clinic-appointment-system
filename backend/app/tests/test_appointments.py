def test_create_appointment(
    test_client,
    patient_token
):

    schedules_response = test_client.get(
        "/schedules/doctor/1"
    )


    assert schedules_response.status_code == 200


    schedules = schedules_response.json()


    assert len(schedules) > 0


    schedule_id = schedules[0]["id"]


    response = test_client.post(
        "/appointments/",
        headers={
            "Authorization":
            f"Bearer {patient_token}"
        },
        json={
            "schedule_id": schedule_id,
            "notes": "test appointment"
        }
    )


    assert response.status_code in [
        200,
        201
    ]



def test_patient_appointments(
    test_client,
    patient_token
):

    response = test_client.get(
        "/appointments/my",
        headers={
            "Authorization":
            f"Bearer {patient_token}"
        }
    )


    assert response.status_code == 200