from sqlalchemy.orm import Session

from ..models.specialty import Specialty
from ..schemas.specialty import SpecialtyCreate
from app.core.logger import logger


def get_all_specialties(
    db: Session,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Specialty)
        .order_by(Specialty.id)
        .offset(skip)
        .limit(limit)
        .all()
    )



def get_specialty_by_code(
    db: Session,
    code: str
):
    return db.query(
        Specialty
    ).filter(
        Specialty.code == code
    ).first()



def get_specialty_by_id(
    db: Session,
    specialty_id: int
):
    return db.query(
        Specialty
    ).filter(
        Specialty.id == specialty_id
    ).first()



def create_specialty(
    db: Session,
    specialty_data: SpecialtyCreate
):

    existing = get_specialty_by_code(
        db,
        specialty_data.code
    )

    if existing:
        return None


    specialty = Specialty(
        code=specialty_data.code.upper(),
        title=specialty_data.title
    )


    db.add(specialty)
    db.commit()
    db.refresh(specialty)
    logger.info(
        f"Specialty created: {specialty.code}"
    )
    return specialty



def update_specialty(
    db: Session,
    code: str,
    title: str
):

    specialty = get_specialty_by_code(
        db,
        code
    )


    if not specialty:
        return None


    specialty.title = title

    db.commit()
    db.refresh(specialty)

    logger.info(
        f"Specialty updated: {specialty.code}"
    )
    return specialty



def delete_specialty(
    db: Session,
    code: str
):

    specialty = get_specialty_by_code(
        db,
        code
    )


    if not specialty:
        return None

    logger.info(
        f"Specialty updated: {specialty.code}"
    )

    db.delete(specialty)
    db.commit()

    return True