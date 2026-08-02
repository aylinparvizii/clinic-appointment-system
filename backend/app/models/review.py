from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id")
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id")
    )

    rating = Column(
        Integer,
        nullable=False
    )

    comment = Column(
        Text,
        nullable=True
    )

    patient = relationship(
        "Patient",
        back_populates="reviews"
    )

    doctor = relationship(
        "Doctor",
        back_populates="reviews"
    )