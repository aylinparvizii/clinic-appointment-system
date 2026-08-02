from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.dependencies import get_db

from ..schemas.specialty import (
    SpecialtyCreate,
    SpecialtyResponse
)

from ..services.specialty_service import (
    get_all_specialties,
    get_specialty_by_code,
    create_specialty,
    delete_specialty,
    update_specialty
)

from ..core.security import get_current_admin


router = APIRouter(
    prefix="/specialties",
    tags=["specialties"]
)


@router.get(
    "/",
    response_model=list[SpecialtyResponse]
)
def list_specialties(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_all_specialties(
        db,
        skip,
        limit
    )


@router.get(
    "/{code}",
    response_model=SpecialtyResponse
)
def get_specialty(
    code: str,
    db: Session = Depends(get_db)
):
    specialty = get_specialty_by_code(
        db,
        code.upper()
    )

    if not specialty:
        raise HTTPException(
            status_code=404,
            detail="Specialty not found"
        )

    return specialty


@router.post(
    "/",
    response_model=SpecialtyResponse
)
def add_specialty(
    specialty: SpecialtyCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    new_specialty = create_specialty(
        db,
        specialty
    )

    if not new_specialty:
        raise HTTPException(
            status_code=400,
            detail="Specialty code already exists"
        )

    return new_specialty


@router.put(
    "/{code}",
    response_model=SpecialtyResponse
)
def edit_specialty(
    code: str,
    title: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    specialty = update_specialty(
        db,
        code.upper(),
        title
    )

    if not specialty:
        raise HTTPException(
            status_code=404,
            detail="Specialty not found"
        )

    return specialty


@router.delete(
    "/{code}"
)
def remove_specialty(
    code: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    deleted = delete_specialty(
        db,
        code.upper()
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Specialty not found"
        )

    return {
        "message": "Specialty deleted successfully"
    }