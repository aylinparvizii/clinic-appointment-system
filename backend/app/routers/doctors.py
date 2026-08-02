from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.dependencies import get_db
from ..core.security import get_current_admin
from ..schemas.doctor import (
    DoctorCreate,
    DoctorResponse
)
from app.core.logger import logger
from ..services.doctor_service import (
    get_all_doctors,
    get_doctor_by_id,
    get_doctors_by_specialty,
    create_doctor_profile,
    update_doctor,
    delete_doctor
)

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"]
)


@router.get(
    "/",
    response_model=list[DoctorResponse]
)
def list_doctors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_all_doctors(
    db,
    skip,
    limit
    )


@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    doctor = get_doctor_by_id(
        db,
        doctor_id
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.get(
    "/specialty/{code}",
    response_model=list[DoctorResponse]
)
def doctors_by_specialty(
    code: str,
    db: Session = Depends(get_db)
):
    return get_doctors_by_specialty(
        db,
        code
    )


@router.post(
    "/",
    response_model=DoctorResponse
)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):

    doctor = create_doctor_profile(
    db,
    doctor.user_id,
    doctor.specialty_code,
    doctor.experience_years
    )

    return doctor


@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def edit_doctor(
    doctor_id: int,
    specialty_code: str | None = None,
    experience_years: int | None = None,
    db: Session = Depends(get_db)
):

    doctor = update_doctor(
        db,
        doctor_id,
        specialty_code,
        experience_years
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.delete(
    "/{doctor_id}"
)
def remove_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    result = delete_doctor(
        db,
        doctor_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )


    return {
        "message": "Doctor deleted successfully"
    }