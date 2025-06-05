from fastapi import APIRouter, Depends, HTTPException, status , Query
from sqlalchemy.orm import Session
from models import User
from services.booking_service import BookingService
from schemas.booking_schema import BookingCreate, BookingOut
from utilities.dependencies import get_db, get_current_user

router = APIRouter(prefix="/bookings", tags=["bookings"])

# POST /bookings
@router.post("/", response_model=BookingOut)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Let the BookingService handle the logic
    booking = BookingService.create_booking(
        db=db,
        class_id=booking_in.class_id,
        user=current_user,
        client_name=booking_in.client_name,
        client_email=booking_in.client_email
    )
    return booking

# GET /bookings
@router.get("/", response_model=list[BookingOut])
def get_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookings = BookingService.get_bookings_by_user(db=db, user=current_user)
    return bookings

@router.get("/by-email", response_model=list[BookingOut])
def get_bookings_by_email(
    email: str = Query(..., description="Email address to filter bookings"),
    db: Session = Depends(get_db)
):
    bookings = BookingService.get_bookings_by_email(db=db, email=email)
    if not bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bookings found for this email.")
    return bookings