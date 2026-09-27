from datetime import datetime

from app.models.schedule import Schedule
from app.services.schedule_service import filter_available_schedules


def create_schedule(status: str):
    return Schedule(
        doctor_id=1,
        start_time=datetime(2026, 9, 27, 9, 0),
        end_time=datetime(2026, 9, 27, 9, 30),
        status=status,
    )


def test_filter_available_schedules():
    available_schedule = create_schedule("available")
    busy_schedule = create_schedule("busy")
    cancelled_schedule = create_schedule("cancelled")

    result = filter_available_schedules(
        [
            available_schedule,
            busy_schedule,
            cancelled_schedule,
        ]
    )

    assert len(result) == 1
    assert result[0].status == "available"


def test_filter_available_schedules_returns_empty_list_when_no_schedule_is_available():
    busy_schedule = create_schedule("busy")
    cancelled_schedule = create_schedule("cancelled")

    result = filter_available_schedules(
        [
            busy_schedule,
            cancelled_schedule,
        ]
    )

    assert result == []


def test_filter_available_schedules_with_empty_list():
    result = filter_available_schedules([])

    assert result == []


def test_filter_available_schedules_returns_multiple_available_schedules():
    schedule_1 = create_schedule("available")
    schedule_2 = create_schedule("available")
    schedule_3 = create_schedule("busy")

    result = filter_available_schedules(
        [
            schedule_1,
            schedule_2,
            schedule_3,
        ]
    )

    assert len(result) == 2
    assert all(
        schedule.status == "available"
        for schedule in result
    )