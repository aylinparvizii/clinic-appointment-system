from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.base import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
        )
    
    doctor_id = Column(
        Integer, 
        ForeignKey("doctors.id"), 
        nullable=False
        )
    
    start_time = Column(
        DateTime, 
        nullable=False
        )  
    
    end_time = Column(
        DateTime, 
        nullable=False
        )   

    status = Column(
        String, 
        default="available"
        )   # available, busy, cancelled
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    # رابطه‌ها
    doctor = relationship("Doctor", back_populates="schedules")
    appointments = relationship("Appointment", back_populates="schedule")