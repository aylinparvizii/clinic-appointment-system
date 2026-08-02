from sqlalchemy.orm import Session

from ..models.schedule import Schedule
from ..schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.core.logger import logger


# ساخت زمان جدید برای دکتر
def create_schedule(
    db: Session,
    schedule_data: ScheduleCreate
):

    schedule = Schedule(
        doctor_id=schedule_data.doctor_id,
        start_time=schedule_data.start_time,
        end_time=schedule_data.end_time,
        status="available"
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    logger.info(
        f"Schedule created. schedule_id={schedule.id}, doctor_id={schedule.doctor_id}"
    )
    return schedule



# گرفتن همه زمان‌های یک دکتر
def get_doctor_schedules(
    db: Session,
    doctor_id: int,
    skip: int = 0,
    limit: int = 10
):

    return (
        db.query(Schedule)
        .filter(
            Schedule.doctor_id == doctor_id
        )
        .order_by(Schedule.id)
        .offset(skip)
        .limit(limit)
        .all()
    )



# گرفتن فقط تایم‌های آزاد یک دکتر
def get_available_schedules(
    db: Session,
    doctor_id: int,
    skip: int = 0,
    limit: int = 10
):

    return (
        db.query(Schedule)
        .filter(
            Schedule.doctor_id == doctor_id,
            Schedule.status == "available"
        )
        .order_by(Schedule.id)
        .offset(skip)
        .limit(limit)
        .all()
    )



# گرفتن یک تایم خاص
def get_schedule_by_id(
    db: Session,
    schedule_id: int
):

    return db.query(
        Schedule
    ).filter(
        Schedule.id == schedule_id
    ).first()



# تغییر وضعیت تایم
def update_schedule_status(
    db: Session,
    schedule_id: int,
    status: str
):

    schedule = get_schedule_by_id(
        db,
        schedule_id
    )

    if not schedule:
        return None


    schedule.status = status

    db.commit()
    db.refresh(schedule)

    return schedule



# ویرایش زمان
def update_schedule(
    db: Session,
    schedule_id: int,
    schedule_data: ScheduleUpdate
):

    schedule = get_schedule_by_id(
        db,
        schedule_id
    )

    if not schedule:
        return None


    schedule.start_time = schedule_data.start_time
    schedule.end_time = schedule_data.end_time
    schedule.status = schedule_data.status


    db.commit()
    db.refresh(schedule)
    logger.info(
        f"Schedule updated. schedule_id={schedule.id}"
    )
    return schedule



# حذف زمان
def delete_schedule(
    db: Session,
    schedule_id: int
):

    schedule = get_schedule_by_id(
        db,
        schedule_id
    )

    if not schedule:
        return None

    logger.info(
        f"Schedule deleted. schedule_id={schedule.id}"
    )
    db.delete(schedule)
    db.commit()

    return True