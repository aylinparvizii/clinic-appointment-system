from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.dependencies import get_db

from ..schemas.visit_record import (
    VisitRecordCreate,
    VisitRecordResponse
)

from ..services.visit_record_service import (
    create_visit_record,
    get_visit_record,
    get_doctor_visit_records
)

from ..core.security import get_current_user


router = APIRouter(
    prefix="/visit-records",
    tags=["visit-records"]
)

@router.post(
    "/",
    response_model=VisitRecordResponse
)
def create_record(
    data: VisitRecordCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "doctor":
        raise HTTPException(
            status_code=403,
            detail="Only doctors can create visit records"
        )

    return create_visit_record(
        db,
        data.appointment_id,
        current_user.doctor_profile.id,
        data.diagnosis,
        data.prescription,
        data.notes
    )
@router.get(
    "/doctor/my",
    response_model=list[VisitRecordResponse]
)
def my_visit_records(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "doctor":
        raise HTTPException(
            status_code=403,
            detail="Only doctors can access records"
        )


    return get_doctor_visit_records(
        db,
        current_user.doctor_profile.id,
        skip,
        limit
    )