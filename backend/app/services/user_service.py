from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserRegister
from ..core.security import hash_password
from app.core.logger import logger

def create_user(
    db: Session,
    user_data: UserRegister
):
    """
    ساخت کاربر جدید
    """

    existing_mobile = db.query(User).filter(
        User.mobile == user_data.mobile
    ).first()

    if existing_mobile:
        return None


    existing_email = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_email:
        return None


    db_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        mobile=user_data.mobile,
        email=user_data.email,
        hashed_password=hash_password(
            user_data.password
        ),
        role=user_data.role,
        gender=user_data.gender,
        birth_date=user_data.birth_date
    )


    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info(
    f"User created: id={db_user.id}, role={db_user.role}"
    )

    return db_user



def get_user_by_mobile(
    db: Session,
    mobile: str
):
    """
    پیدا کردن کاربر برای لاگین
    """

    return db.query(
        User
    ).filter(
        User.mobile == mobile
    ).first()



def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(
        User
    ).filter(
        User.email == email
    ).first()



def get_user_by_id(
    db: Session,
    user_id: int
):

    return db.query(
        User
    ).filter(
        User.id == user_id
    ).first()



def get_all_users(
    db: Session,
    skip: int = 0,
    limit: int = 10
):

    return (
        db.query(User)
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )



def get_users_by_role(
    db: Session,
    role: str
):

    return db.query(
        User
    ).filter(
        User.role == role
    ).all()



def update_user_status(
    db: Session,
    user_id: int,
    is_active: bool
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        return None


    user.is_active = is_active

    db.commit()
    db.refresh(user)

    logger.info(
    f"User status updated: id={user.id}, active={user.is_active}"
    )

    return user



def change_user_role(
    db: Session,
    user_id: int,
    role: str
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        return None


    user.role = role

    db.commit()
    db.refresh(user)

    logger.info(
        f"User role changed: id={user.id}, role={user.role}"
    )

    return user