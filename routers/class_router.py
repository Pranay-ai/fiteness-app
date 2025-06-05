from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
from schemas.class_schema import ClassCreate, ClassOut
from services import FitnessClassService
from  utilities import dependencies

router = APIRouter(prefix="/classes", tags=["classes"])


@router.get("/", response_model=list[ClassOut])
def get_all_classes(db: Session = Depends(dependencies.get_db)):
    classes = FitnessClassService.get_all_classes(db)
    return classes


@router.post("/", response_model=ClassOut)
def create_class(
    class_in: ClassCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: User = Depends(dependencies.get_current_user)
):
    fitness_class = FitnessClassService.create_class(
        db=db,
        instructor=current_user,
        name=class_in.name,
        start_time_ist=class_in.start_time,
        end_time_ist=class_in.end_time,
        available_slots=class_in.available_slots
    )
    return fitness_class
