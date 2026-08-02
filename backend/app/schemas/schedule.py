from datetime import datetime
from pydantic import BaseModel

class ScheduleBase(BaseModel):
    doctor_id: int
    start_time: datetime
    end_time: datetime
    status: str = "available"

class ScheduleCreate(BaseModel):
    start_time: datetime
    end_time: datetime

class ScheduleResponse(BaseModel):
    id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime
    status: str

    class Config:
        from_attributes = True
        
class ScheduleUpdate(BaseModel):
    start_time: datetime
    end_time: datetime
    status: str