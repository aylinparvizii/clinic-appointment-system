
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    mobile = Column(
        String(20),
        unique=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False
    )

    birth_date = Column(
      Date,
      nullable=True
    )

    gender = Column(
        String(10),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
      DateTime,
      default=datetime.utcnow
    )

    updated_at = Column(
    DateTime,
      default=datetime.utcnow,
      onupdate=datetime.utcnow
    )

    doctor_profile = relationship(
        "Doctor",
        back_populates="user",
        uselist=False
    )

    patient_profile = relationship(
        "Patient",
        back_populates="user",
        uselist=False
    )
