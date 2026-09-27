import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock

from app.services.appointment_service import create_appointment


def mock_schedule(db, status="available"):
    schedule = MagicMock()
    schedule.id = 1
    schedule.doctor_id = 10
    schedule.status = status

    db.query.return_value.with_hint.return_value.filter.return_value.first.return_value = schedule

    return schedule


# 1. رزرو تایم آزاد باید با موفقیت انجام شود
def test_create_appointment_with_available_schedule():

    db = MagicMock()

    schedule = mock_schedule(db, "available")

    appointment = MagicMock()
    appointment.id = 100

    db.add.side_effect = lambda obj: None
    db.commit.side_effect = lambda: None
    db.refresh.side_effect = lambda obj: None

    result = create_appointment(
        db=db,
        patient_id=5,
        schedule_id=1
    )

    # تایم باید busy شود
    assert schedule.status == "busy"

    # رزرو باید به database اضافه شود
    db.add.assert_called_once()

    # commit باید انجام شود
    db.commit.assert_called_once()


# 2. رزرو تایم busy نباید امکان‌پذیر باشد
def test_create_appointment_when_schedule_is_busy():

    db = MagicMock()

    schedule = mock_schedule(db, "busy")

    with pytest.raises(HTTPException) as exc_info:
        create_appointment(
            db=db,
            patient_id=5,
            schedule_id=1
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Schedule is not available"

    db.add.assert_not_called()
    db.commit.assert_not_called()


# 3. رزرو تایمی که وجود ندارد باید 404 بدهد
def test_create_appointment_when_schedule_not_found():

    db = MagicMock()

    db.query.return_value.with_hint.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        create_appointment(
            db=db,
            patient_id=5,
            schedule_id=999
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Schedule not found"

    db.add.assert_not_called()
    db.commit.assert_not_called()


# 4. وقتی رزرو موفق است، patient و schedule درست استفاده شوند
def test_create_appointment_uses_correct_patient_and_schedule():

    db = MagicMock()

    schedule = mock_schedule(db, "available")

    db.commit.side_effect = lambda: None
    db.refresh.side_effect = lambda obj: None

    result = create_appointment(
        db=db,
        patient_id=25,
        schedule_id=1,
        notes="First visit"
    )

    # Appointment ساخته شده باید در db.add قرار گرفته باشد
    db.add.assert_called_once()

    appointment = db.add.call_args[0][0]

    assert appointment.patient_id == 25
    assert appointment.doctor_id == 10
    assert appointment.schedule_id == 1
    assert appointment.status == "scheduled"
    assert appointment.notes == "First visit"

    # schedule باید بعد از رزرو busy شود
    assert schedule.status == "busy"