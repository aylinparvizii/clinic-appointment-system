from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
        )
    
    patient_id = Column(
        Integer, 
        ForeignKey("patients.id"), 
        nullable=False
        )
    
    doctor_id = Column(
        Integer, 
        ForeignKey("doctors.id"), 
        nullable=False
        )
    schedule_id = Column(
        Integer, 
        ForeignKey("schedules.id"), 
        nullable=False
        )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
        )
    status = Column(
        String(20),
        default="scheduled",
        nullable=False
        )  # scheduled, completed, cancelled
    
    notes = Column(
        Text,
        nullable=True
        )     
         # توضیحات بیمار یا پزشک

    # رابطه‌ها

    patient = relationship(
        "Patient", 
        back_populates="appointments"
        )
    
    doctor = relationship(
        "Doctor", 
        back_populates="appointments"
        )
    
    schedule = relationship(
        "Schedule", 
        back_populates="appointments"
        )
    
    visit_record = relationship(
        "VisitRecord", 
        back_populates="appointment", 
        uselist=False
        )