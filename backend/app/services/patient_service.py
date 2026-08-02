from sqlalchemy.orm import Session
from app.core.logger import logger
from ..models.patient import Patient



def get_all_patients(
    db: Session,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Patient)
        .order_by(Patient.id)
        .offset(skip)
        .limit(limit)
        .all()
    )



def get_patient_by_id(
    db: Session,
    patient_id: int
):
    return db.query(
        Patient
    ).filter(
        Patient.id == patient_id
    ).first()



def get_patient_by_user_id(
    db: Session,
    user_id: int
):
    return db.query(
        Patient
    ).filter(
        Patient.user_id == user_id
    ).first()



def create_patient_profile(
    db: Session,
    user_id: int,
    medical_history: str | None = None,
    medications: str | None = None
):

    patient = Patient(
        user_id=user_id,
        medical_history=medical_history,
        medications=medications
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    logger.info(
    f"Patient profile created. patient_id={patient.id}"
    )

    return patient



def update_patient(
    db: Session,
    patient_id: int,
    medical_history: str | None = None,
    medications: str | None = None
):

    patient = get_patient_by_id(
        db,
        patient_id
    )

    if not patient:
        return None


    if medical_history is not None:
        patient.medical_history = medical_history


    if medications is not None:
        patient.medications = medications


    db.commit()
    db.refresh(patient)

    return patient



def delete_patient(
    db: Session,
    patient_id: int
):

    patient = get_patient_by_id(
        db,
        patient_id
    )

    if not patient:
        return None

    logger.info(
        f"Patient profile created. patient_id={patient.id}"
    )

    db.delete(patient)
    db.commit()

    return True