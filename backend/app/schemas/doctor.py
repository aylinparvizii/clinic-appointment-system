from pydantic import BaseModel


class DoctorCreate(BaseModel):
    specialty_code: str
    experience_years: int


class DoctorUpdate(BaseModel):
    specialty_code: str
    experience_years: int


class DoctorResponse(BaseModel):
    id: int
    user_id: int
    specialty_code: str
    experience_years: int

    class Config:
        from_attributes = True