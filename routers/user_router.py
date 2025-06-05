from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas , services

from  utilities import dependencies


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    user = services.UserService.create_user(
        db=db,
        username=user.username,
        email=user.email,
        password=user.password,
        is_coach=user.is_coach
    )
    return user



@router.post("/login", response_model=schemas.Token)
def login(user_in: schemas.UserLogin, db: Session = Depends(dependencies.get_db)):
    user = services.UserService.authenticate_user(db, user_in.username, user_in.password)
    access_token = services.UserService.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}