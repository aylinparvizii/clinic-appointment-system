from pydantic import BaseModel , Field


class ReviewCreate(BaseModel):
    doctor_id: int
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


class ReviewResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    rating: int
    comment: str | None = None

    class Config:
        from_attributes = True