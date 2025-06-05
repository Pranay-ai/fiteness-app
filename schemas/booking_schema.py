from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    class_id: int
    # These could also come from the user, but keeping them explicit is fine:
    client_name: str
    client_email: str

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: str
    created_at: datetime

    class Config:
        orm_mode = True