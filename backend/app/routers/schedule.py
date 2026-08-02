from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.dependencies import get_db
from ..models.schedule import Schedule
from ..models.doctor import Doctor
from ..schemas.schedule import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse
)

from ..core.security import get_current_user


router = APIRouter(
    prefix="/schedules",
    tags=["schedules"]
)


# ----------------------------------
# مشاهده تایم های آزاد یک دکتر
# برای بیمار
# ----------------------------------

@router.get(
    "/doctor/{doctor_id}",
    response_model=list[ScheduleResponse]
)
def get_doctor_schedules(
    doctor_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    schedules = (
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
    return schedules



# ----------------------------------
# مشاهده تایم های خود دکتر
# ----------------------------------

@router.get(
    "/my",
    response_model=list[ScheduleResponse]
)
def get_my_schedules(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "doctor":
        raise HTTPException(
            status_code=403,
            detail="Only doctors can access schedules"
        )


    doctor = current_user.doctor_profile

    schedules = (
        db.query(Schedule)
        .filter(
            Schedule.doctor_id == doctor.id
        )
        .order_by(Schedule.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return schedules



# ----------------------------------
# ساخت تایم جدید توسط دکتر
# ----------------------------------

@router.post(
    "/",
    response_model=ScheduleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_schedule(
    data: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "doctor":
        raise HTTPException(
            status_code=403,
            detail="Only doctors can create schedules"
        )


    doctor = current_user.doctor_profile


    if data.end_time <= data.start_time:
        raise HTTPException(
            status_code=400,
            detail="Invalid time range"
        )


    schedule = Schedule(
        doctor_id=doctor.id,
        start_time=data.start_time,
        end_time=data.end_time,
        status="available"
    )


    db.add(schedule)
    db.commit()
    db.refresh(schedule)


    return schedule



# ----------------------------------
# تغییر تایم
# فقط دکتر خودش
# ----------------------------------

@router.put(
    "/{schedule_id}",
    response_model=ScheduleResponse
)
def update_schedule(
    schedule_id: int,
    data: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
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


    if schedule.doctor_id != current_user.doctor_profile.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot edit this schedule"
        )


    schedule.start_time = data.start_time
    schedule.end_time = data.end_time
    schedule.status = data.status


    db.commit()
    db.refresh(schedule)


    return schedule



# ----------------------------------
# حذف تایم
# ----------------------------------

@router.delete(
    "/{schedule_id}"
)
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
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


    if schedule.doctor_id != current_user.doctor_profile.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this schedule"
        )


    if schedule.status == "busy":
        raise HTTPException(
            status_code=400,
            detail="Reserved schedule cannot be deleted"
        )


    db.delete(schedule)
    db.commit()


    return {
        "message": "Schedule deleted successfully"
    }