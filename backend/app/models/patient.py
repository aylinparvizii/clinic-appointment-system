from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable = False
    )

    medical_history = Column(
        Text,
        nullable=True
    )

    medications = Column(
        Text,
        nullable=True
    )


    user = relationship(
        "User",
        back_populates="patient_profile"
    )

    appointments = relationship(
        "Appointment",
        back_populates="patient"
    )

    reviews = relationship(
        "Review",
        back_populates="patient"
    )