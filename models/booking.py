from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("fitness_classes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # NEW
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    fitness_class = relationship("FitnessClass", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
