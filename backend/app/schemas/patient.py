from pydantic import BaseModel


class PatientCreate(BaseModel):
    medical_history: str | None = None
    medications: str | None = None


class PatientResponse(BaseModel):
    id: int
    user_id: int
    medical_history: str | None = None
    medications: str | None = None

    class Config:
        from_attributes = True