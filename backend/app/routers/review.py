from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.dependencies import get_db

from ..schemas.review import (
    ReviewCreate,
    ReviewResponse
)

from ..services.review_service import (
    create_review,
    get_doctor_reviews
)

from ..core.security import get_current_user


router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)


@router.post(
    "/",
    response_model=ReviewResponse
)
def add_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can submit reviews"
        )

    return create_review(
        db,
        current_user.patient_profile.id,
        review_data.doctor_id,
        review_data.rating,
        review_data.comment
    )  


@router.get(
    "/doctor/{doctor_id}",
    response_model=list[ReviewResponse]
)
def doctor_reviews(
    doctor_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    return get_doctor_reviews(
        db,
        doctor_id,
        skip,
        limit
    )