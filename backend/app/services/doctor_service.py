from sqlalchemy.orm import Session

from ..models.doctor import Doctor
from ..models.specialty import Specialty
from ..schemas.doctor import DoctorCreate
from app.core.logger import logger
from fastapi import HTTPException

def get_all_doctors(
    db: Session,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Doctor)
        .order_by(Doctor.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_doctor_by_id(
    db: Session,
    doctor_id: int
):
    return db.query(
        Doctor
    ).filter(
        Doctor.id == doctor_id
    ).first()


def get_doctor_by_user_id(
    db: Session,
    user_id: int
):
    return db.query(
        Doctor
    ).filter(
        Doctor.user_id == user_id
    ).first()


def get_doctors_by_specialty(
    db: Session,
    specialty_code: str
):
    return db.query(
        Doctor
    ).filter(
        Doctor.specialty_code == specialty_code
    ).all()



def create_doctor_profile(
    db: Session,
    user_id: int,
    specialty_code: str,
    experience_years: int
):
    specialty = db.query(Specialty).filter(
        Specialty.code == specialty_code
    ).first()

    if not specialty:
        raise HTTPException(
            status_code=404,
            detail="Specialty not found"
        )
    doctor = Doctor(
        user_id=user_id,
        specialty_code=specialty_code,
        experience_years=experience_years
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    logger.info(
    f"Doctor profile created. doctor_id={doctor.id}"
    )
    return doctor



def update_doctor(
    db: Session,
    doctor_id: int,
    specialty_code: str | None = None,
    experience_years: int | None = None
):

    doctor = get_doctor_by_id(
        db,
        doctor_id
    )

    if not doctor:
        return None


    if specialty_code:

        specialty = db.query(Specialty).filter(
            Specialty.code == specialty_code
        ).first()

        if not specialty:
            raise HTTPException(
                status_code=404,
                detail="Specialty not found"
            )

        doctor.specialty_code = specialty_code


    if experience_years is not None:
        doctor.experience_years = experience_years


    db.commit()

    logger.info(
    f"Doctor updated. doctor_id={doctor.id}"
    )
    db.refresh(doctor)

    return doctor



def delete_doctor(
    db: Session,
    doctor_id: int
):

    doctor = get_doctor_by_id(
        db,
        doctor_id
    )

    if not doctor:
        return None

    logger.info(
    f"Doctor deleted. doctor_id={doctor.id}"
    )

    db.delete(doctor)
    db.commit()

    return True