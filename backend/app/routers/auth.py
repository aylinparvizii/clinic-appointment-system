from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.dependencies import get_db
from ..models.user import User
from ..schemas.user import (
    UserLogin,
    UserRegister,
    UserResponse
)
from app.core.logger import logger
from ..core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=UserResponse)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    # چک شماره موبایل
    existing_mobile = db.query(User).filter(
        User.mobile == user.mobile
    ).first()

    if existing_mobile:
        raise HTTPException(
            status_code=400,
            detail="Mobile already registered"
        )


    # چک ایمیل
    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    hashed_password = hash_password(
        user.password
    )


    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        mobile=user.mobile,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        gender=user.gender,
        birth_date=user.birth_date
    )


    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info(
        f"New user registered: {user.mobile}"
    )
    return db_user



@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.mobile == user.mobile
    ).first()


    if not db_user:

        logger.warning(
            f"Login failed. Mobile {user.mobile} not found"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid mobile or password"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):

        logger.warning(
            f"Wrong password for user {db_user.mobile}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid mobile or password"
        )


    token = create_access_token(
        data={
            "sub": str(db_user.id),
            "role": db_user.role
        }
    )

    logger.info(
        f"User logged in: {user.mobile}"
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }



@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    logger.info(
    f"User {current_user.id} requested profile"
)

    return current_user