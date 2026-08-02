
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..database.base import Base

class VisitRecord(Base):
    __tablename__ = "visit_records"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    diagnosis = Column(Text, nullable=True)        # تشخیص پزشک
    prescription = Column(Text, nullable=True)     # نسخه
    notes = Column(Text, nullable=True)             # توضیحات اضافی
    visit_date = Column(DateTime, nullable=False)

    # رابطه‌ها
    appointment = relationship("Appointment", back_populates="visit_record")
    doctor = relationship("Doctor", back_populates="visit_records")