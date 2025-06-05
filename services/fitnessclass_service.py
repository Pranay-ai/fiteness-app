# services/class_service.py

from sqlalchemy.orm import Session
from models import FitnessClass, User
from fastapi import HTTPException, status
from datetime import datetime
import pytz

class FitnessClassService:

    @staticmethod
    def create_class(
        db: Session,
        instructor: User,
        name: str,
        start_time_ist: datetime,
        end_time_ist: datetime,
        available_slots: int
    ):

        if not bool(instructor.is_coach):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only coaches can create classes."
            )
        

        ist = pytz.timezone("Asia/Kolkata")
        start_time_utc = ist.localize(start_time_ist).astimezone(pytz.utc)
        end_time_utc = ist.localize(end_time_ist).astimezone(pytz.utc)


        overlapping_class = db.query(FitnessClass).filter(
            FitnessClass.instructor_id == instructor.id,
            FitnessClass.start_time < end_time_utc,
            FitnessClass.end_time > start_time_utc
        ).first()

        if overlapping_class:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Overlapping class exists."
            )
        

        fitness_class = FitnessClass(
            name=name,
            instructor_id=instructor.id,
            start_time=start_time_utc,
            end_time=end_time_utc,
            available_slots=available_slots
        )
        db.add(fitness_class)
        db.commit()
        db.refresh(fitness_class)

        return fitness_class

    @staticmethod
    def get_all_classes(db: Session):
        return db.query(FitnessClass).all()
