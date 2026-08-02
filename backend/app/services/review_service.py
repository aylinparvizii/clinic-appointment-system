from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.logger import logger
from ..models.review import Review
from ..models.appointment import Appointment



# =========================
# ثبت نظر بیمار
# =========================

def create_review(
    db: Session,
    patient_id: int,
    doctor_id: int,
    rating: int,
    comment: str | None = None
):


    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5"
        )

    # جلوگیری از ثبت نظر تکراری
    review_exists = db.query(Review).filter(
        Review.patient_id == patient_id,
        Review.doctor_id == doctor_id
    ).first()


    if review_exists:
        raise HTTPException(
            status_code=400,
            detail="You already reviewed this doctor"
        )
    # چک کنیم بیمار واقعا پیش این دکتر رفته
    appointment = db.query(
        Appointment
    ).filter(
        Appointment.patient_id == patient_id,
        Appointment.doctor_id == doctor_id,
        Appointment.status == "completed"
    ).first()


    if not appointment:
        raise HTTPException(
            status_code=403,
            detail="You can review only completed appointments"
        )



    review = Review(
        patient_id=patient_id,
        doctor_id=doctor_id,
        rating=rating,
        comment=comment
    )


    db.add(review)

    db.commit()

    db.refresh(review)

    logger.info(
        f"Review created. review_id={review.id}, patient_id={patient_id}, doctor_id={doctor_id}"
    )

    return review



# =========================
# گرفتن نظرات یک پزشک
# =========================

def get_doctor_reviews(
    db: Session,
    doctor_id: int,
    skip: int = 0,
    limit: int = 10
):

    return (
        db.query(Review)
        .order_by(Review.id)
        .filter(
            Review.doctor_id == doctor_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )



# =========================
# گرفتن نظرات بیمار
# =========================

def get_patient_reviews(
    db: Session,
    patient_id: int
):

    return db.query(
        Review
    ).filter(
        Review.patient_id == patient_id
    ).all()



# =========================
# میانگین امتیاز پزشک
# =========================

def get_doctor_rating(
    db: Session,
    doctor_id: int
):

    reviews = db.query(
        Review
    ).filter(
        Review.doctor_id == doctor_id
    ).all()


    if not reviews:
        return {
            "average": 0,
            "count":0
        }


    avg = sum(
        r.rating for r in reviews
    ) / len(reviews)


    return {
        "average": round(avg,2),
        "count":len(reviews)
    }



# =========================
# حذف نظر
# =========================

def delete_review(
    db: Session,
    review_id:int
):

    review = db.query(
        Review
    ).filter(
        Review.id == review_id
    ).first()


    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    logger.info(
        f"Review deleted. review_id={review.id}"
    )
    db.delete(review)

    db.commit()


    return True