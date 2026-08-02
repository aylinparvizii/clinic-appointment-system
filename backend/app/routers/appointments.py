from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.dependencies import get_db

from ..schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse
)
from app.core.logger import logger
from ..services.appointment_service import (
    create_appointment,
    get_patient_appointments,
    get_doctor_appointments,
    cancel_appointment
)

from ..core.security import get_current_user


router = APIRouter(
    prefix="/appointments",
    tags=["appointments"]
)


@router.post(
    "/",
    response_model=AppointmentResponse
)
def reserve_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can reserve appointments"
        )

    appointment = create_appointment(
        db,
        current_user.patient_profile.id,
        appointment_data.schedule_id,
        appointment_data.notes
    )


    logger.info(
        f"Appointment created: {appointment.id} by patient {current_user.id}"
    )


    return appointment


@router.get(
    "/my",
    response_model=list[AppointmentResponse]
)
def my_appointments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can access appointments"
        )
    
    logger.info(
        f"Patient {current_user.id} viewed own appointments"
    )
    return get_patient_appointments(
        db,
        current_user.patient_profile.id,
        skip,
        limit
    )


@router.get(
    "/doctor/my",
    response_model=list[AppointmentResponse]
)
def doctor_appointments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "doctor":
        raise HTTPException(
            status_code=403,
            detail="Only doctors can access appointments"
        )
    
    logger.info(
    f"Doctor {current_user.id} viewed appointments"
   )

    return get_doctor_appointments(
        db,
        current_user.doctor_profile.id,
        skip,
        limit
    )


@router.delete(
    "/{appointment_id}"
)
def cancel(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    appointment = cancel_appointment(
        db,
        appointment_id,
        current_user.id
    )

    logger.info(
        f"Appointment {appointment.id} cancelled by patient {current_user.id}"
    )

    return appointment