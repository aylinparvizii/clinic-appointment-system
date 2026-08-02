
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    specialty_code = Column(
        String(3),
        ForeignKey("specialties.code"),
        nullable=False
    )

    experience_years = Column(
        Integer,
        default=0
    )


#روابط
    user = relationship(
        "User",
        back_populates="doctor_profile"
    )
    specialty = relationship(
        "Specialty",
        back_populates="doctors"
    )

    schedules = relationship(
        "Schedule",
        back_populates="doctor"
    )

    appointments = relationship(
        "Appointment",
        back_populates="doctor"
    )

    visit_records = relationship(
        "VisitRecord",
        back_populates="doctor"
    )
    reviews = relationship(
        "Review",
        back_populates="doctor"
    )