from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.appointment import Appointment
from ..models.schedule import Schedule
from app.core.logger import logger

# ==========================
# ایجاد رزرو
# ==========================

def create_appointment(
    db: Session,
    patient_id: int,
    schedule_id: int,
    notes: str | None = None
):

    schedule = db.query(
        Schedule
    ).filter(
        Schedule.id == schedule_id
    ).first()


    if not schedule:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found"
        )


    if schedule.status != "available":
        raise HTTPException(
            status_code=400,
            detail="Schedule is not available"
        )


    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=schedule.doctor_id,
        schedule_id=schedule.id,
        status="scheduled",
        notes=notes
    )


    schedule.status = "busy"


    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    logger.info(
        f"Appointment {appointment.id} saved in database"
    )
    return appointment
# ==========================
# گرفتن یک رزرو
# ==========================

def get_appointment(
    db: Session,
    appointment_id: int
):

    appointment = db.query(
        Appointment
    ).filter(
        Appointment.id == appointment_id
    ).first()


    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )


    return appointment



# ==========================
# رزروهای یک بیمار
# ==========================

def get_patient_appointments(
    db: Session,
    patient_id: int,
    skip: int = 0,
    limit: int = 10
):

    return (
        db.query(Appointment)
        .order_by(Appointment.id)
        .filter(Appointment.patient_id == patient_id)
        .offset(skip)
        .limit(limit)
        .all()
    )



# ==========================
# رزروهای یک دکتر
# ==========================

def get_doctor_appointments(
    db: Session,
    doctor_id: int,
    skip: int = 0,
    limit: int = 10
):

    return (
        db.query(Appointment)
        .filter(Appointment.doctor_id == doctor_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# ==========================
# رزروهای امروز دکتر
# ==========================

def get_today_doctor_appointments(
    db: Session,
    doctor_id: int,
    skip: int = 0,
    limit: int = 10
):

    from datetime import date


    return (
    db.query(Appointment)
    .filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_time >= date.today()
    )
    .offset(skip)
    .limit(limit)
    .all()
    )



# ==========================
# تغییر وضعیت رزرو
# ==========================

def update_appointment_status(
    db: Session,
    appointment_id: int,
    new_status: str
):

    appointment = get_appointment(
        db,
        appointment_id
    )


    allowed_status = [
        "scheduled",
        "completed",
        "cancelled"
    ]


    if new_status not in allowed_status:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )


    appointment.status = new_status


    # اگر لغو شد دوباره تایم آزاد شود
    if new_status == "cancelled":

        schedule = db.query(
            Schedule
        ).filter(
            Schedule.id == appointment.schedule_id
        ).first()


        if schedule:
            schedule.status = "available"


    db.commit()
    db.refresh(appointment)

    logger.info(
        f"Appointment {appointment.id} status changed to {new_status}"
    )

    return appointment



# ==========================
# لغو رزرو توسط بیمار
# ==========================

def cancel_appointment(
    db: Session,
    appointment_id: int,
    patient_id: int
):

    appointment = db.query(
        Appointment
    ).filter(
        Appointment.id == appointment_id,
        Appointment.patient_id == patient_id
    ).first()


    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )


    appointment.status = "cancelled"


    schedule = db.query(
        Schedule
    ).filter(
        Schedule.id == appointment.schedule_id
    ).first()


    if schedule:
        schedule.status = "available"


    db.commit()
    db.refresh(appointment)

    logger.info(
    f"Appointment {appointment.id} cancelled"
    )
    return appointment



# ==========================
# حذف رزرو (ادمین)
# ==========================

def delete_appointment(
    db: Session,
    appointment_id: int
):

    appointment = get_appointment(
        db,
        appointment_id
    )

    logger.info(
        f"Appointment {appointment.id} deleted"
    )
    db.delete(appointment)
    db.commit()


    return True