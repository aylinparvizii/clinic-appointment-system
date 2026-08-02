from datetime import datetime
from pydantic import BaseModel

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    schedule_id: int
    appointment_time: datetime
    status: str = "scheduled"
    notes: str | None = None

class AppointmentCreate(BaseModel):
    schedule_id: int
    notes: str | None = None

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    schedule_id: int
    status: str
    notes: str | None = None

    class Config:
        from_attributes = True