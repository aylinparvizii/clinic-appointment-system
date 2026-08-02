from pydantic import BaseModel , Field


class SpecialtyCreate(BaseModel):
    code: str = Field(min_length=3, max_length=3)
    title: str


class SpecialtyResponse(BaseModel):
    id: int
    code: str
    title: str

    class Config:
        from_attributes = True