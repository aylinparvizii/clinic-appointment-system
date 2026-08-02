def test_patient_cannot_create_schedule(
    test_client,
    patient_token
):

    response=test_client.post(
        "/schedules/",
        headers={
            "Authorization":
            f"Bearer {patient_token}"
        },
        json={
            "start_time":"2026-07-30T09:00:00",
            "end_time":"2026-07-30T09:30:00"
        }
    )


    assert response.status_code==403