from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from models import FitnessClass, Booking, User  # adjust as needed
from datetime import datetime

class BookingService:

    @staticmethod
    def create_booking(db: Session, class_id: int, user: User, client_name: str, client_email: str):
        # 1. Fetch the class
        fitness_class = db.query(FitnessClass).filter(FitnessClass.id == class_id).with_for_update().first()
        if not fitness_class:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fitness class not found.")
        
        # 2. Prevent booking by instructor (coach)
        if fitness_class.instructor_id == user.id: # type: ignore
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Instructors cannot book their own classes.")

        # 3. Check available slots
        available_slots = fitness_class.available_slots
        if available_slots <= 0: # type: ignore
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No slots available.")
        
        # 4. Decrement slots
        fitness_class.available_slots -= 1 # type: ignore

        # 5. Create booking
        booking = Booking(
            class_id=class_id,
            user_id=user.id,
            client_name=client_name,
            client_email=client_email,
            created_at=datetime.utcnow()
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking


    @staticmethod
    def get_bookings_by_user(db: Session, user: User):
        bookings = db.query(Booking).filter(Booking.user_id == user.id).all()
        return bookings

    @staticmethod
    def get_bookings_by_email(db: Session, email: str):
        bookings = db.query(Booking).filter(Booking.client_email == email).all()
        return bookings
