from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.dependencies import get_db

from ..schemas.user import (
    UserRegister,
    UserResponse
)
from ..core.security import get_current_user, get_current_admin
from ..services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    get_users_by_role,
    update_user_status,
    change_user_role
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "/",
    response_model=UserResponse
)
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    db_user = create_user(
        db,
        user
    )

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    return db_user


@router.get(
    "/",
    response_model=list[UserResponse]
)
def list_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    return get_all_users(
        db,
        skip,
        limit
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.get(
    "/role/{role}",
    response_model=list[UserResponse]
)
def users_by_role(
    role: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    return get_users_by_role(
        db,
        role
    )


@router.patch(
    "/{user_id}/status"
)
def change_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db)
):

    user = update_user_status(
        db,
        user_id,
        is_active
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.patch(
    "/{user_id}/role"
)
def update_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db)
):

    user = change_user_role(
        db,
        user_id,
        role
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user