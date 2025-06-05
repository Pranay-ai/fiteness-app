from sqlalchemy import Column, Integer, String , ForeignKey , DateTime
from sqlalchemy.orm import relationship
from database import Base


class FitnessClass(Base):
    __tablename__ = "fitness_classes"

    id = Column(Integer , primary_key =True , index =True)
    name = Column(String , nullable=False)
    instructor_id = Column(Integer ,ForeignKey('users.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    available_slots = Column(Integer, nullable=False)

    instructor = relationship("User", back_populates="classes_created")