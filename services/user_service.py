import bcrypt
import jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException, status

import models

SECRET_KEY = "supersecretkey"  # In production, load from environment!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserService:
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str , is_coach: int = 0):
        # Check if username or email already exists
        existing_user = db.query(models.User).filter(
            (models.User.username == username) | (models.User.email == email)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username or email already exists."
            )
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = models.User(
            username=username,
            email=email,
            password=hashed_password.decode('utf-8'),
            is_coach=is_coach
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(models.User).filter(models.User.username == username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt