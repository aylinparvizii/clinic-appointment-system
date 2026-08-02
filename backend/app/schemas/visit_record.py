from pydantic import BaseModel
from datetime import datetime


class VisitRecordCreate(BaseModel):
    appointment_id: int
    diagnosis: str
    prescription: str | None = None
    notes: str | None = None


class VisitRecordResponse(BaseModel):
    id: int
    appointment_id: int
    doctor_id: int
    diagnosis: str
    prescription: str | None = None
    notes: str | None = None
    visit_date: datetime

    class Config:
        from_attributes = True