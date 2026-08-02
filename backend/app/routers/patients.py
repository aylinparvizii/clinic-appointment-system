from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.dependencies import get_db

from ..schemas.patient import (
    PatientCreate,
    PatientResponse
)
from ..core.security import get_current_user
from ..services.patient_service import (
    get_all_patients,
    get_patient_by_id,
    create_patient_profile,
    update_patient,
    delete_patient
)

router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)


@router.get(
    "/",
    response_model=list[PatientResponse]
)
def list_patients(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_all_patients(
        db,
        skip,
        limit
    )


@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = get_patient_by_id(
        db,
        patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


@router.post(
    "/",
    response_model=PatientResponse
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):

    return create_patient_profile(
        db,
        patient.user_id,
        patient.medical_history,
        patient.medications
    )


@router.put(
    "/{patient_id}",
    response_model=PatientResponse
)
def edit_patient(
    patient_id: int,
    medical_history: str | None = None,
    medications: str | None = None,
    db: Session = Depends(get_db)
):

    patient = update_patient(
        db,
        patient_id,
        medical_history,
        medications
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


@router.delete(
    "/{patient_id}"
)
def remove_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete patients"
        )

    return {
        "message": "Patient deleted successfully"
    }