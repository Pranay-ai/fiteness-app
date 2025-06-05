from pydantic import BaseModel, Field , field_serializer
from datetime import datetime

class ClassCreate(BaseModel):
    name: str = Field(..., examples=["Yoga"])
    start_time: datetime = Field(..., examples=["2025-06-05 10:00:00"])
    end_time: datetime = Field(..., examples=["2025-06-05 11:00:00"])
    available_slots: int = Field(..., examples=[20])

class ClassOut(BaseModel):
    id: int
    name: str
    start_time: datetime  # returned in IST by router/service
    end_time: datetime    # returned in IST by router/service
    available_slots: int

    class Config:
        orm_mode = True
