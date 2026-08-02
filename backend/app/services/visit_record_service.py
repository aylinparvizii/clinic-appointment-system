from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.visit_record import VisitRecord
from ..models.appointment import Appointment
from datetime import datetime, timezone
from app.core.logger import logger
# =========================
# ایجاد گزارش ویزیت
# =========================

def create_visit_record(
    db: Session,
    appointment_id: int,
    doctor_id: int,
    diagnosis: str,
    prescription: str | None = None,
    notes: str | None = None
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


    if appointment.doctor_id != doctor_id:
        raise HTTPException(
            status_code=403,
            detail="Doctor is not owner of this appointment"
        )


    # فقط وقتی ویزیت انجام شده باشد
    appointment.status = "completed"


    visit = VisitRecord(
        appointment_id=appointment_id,
        doctor_id=doctor_id,
        diagnosis=diagnosis,
        prescription=prescription,
        notes=notes,
        visit_date=datetime.now(timezone.utc)
    )


    db.add(visit)

    db.commit()

    db.refresh(visit)

    logger.info(
        f"Visit record created: id={visit.id}, doctor={doctor_id}, appointment={appointment_id}"
    )
    return visit



# =========================
# گرفتن اطلاعات یک ویزیت
# =========================

def get_visit_record(
    db: Session,
    visit_id: int
):

    visit = db.query(
        VisitRecord
    ).filter(
        VisitRecord.id == visit_id
    ).first()


    if not visit:
        raise HTTPException(
            status_code=404,
            detail="Visit record not found"
        )


    return visit



# =========================
# ویزیت های یک بیمار
# =========================

def get_patient_visit_history(
    db: Session,
    patient_id: int
):

    return db.query(
        VisitRecord
    ).join(
        Appointment
    ).filter(
        Appointment.patient_id == patient_id
    ).all()



# =========================
# ویزیت های یک پزشک
# =========================

def get_doctor_visit_records(
    db: Session,
    doctor_id: int,
    skip: int = 0,
    limit: int = 10
):

    return (
        db.query(VisitRecord)
        .order_by(VisitRecord.id)
        .filter(
            VisitRecord.doctor_id == doctor_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


# =========================
# حذف گزارش ویزیت
# =========================

def delete_visit_record(
    db: Session,
    visit_id: int
):

    visit = get_visit_record(
        db,
        visit_id
    )

    logger.info(
        f"Visit record deleted: id={visit.id}"
    )
    db.delete(visit)

    db.commit()


    return True