from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker, declarative_base

# Database connection string
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "postgresql://postgres:root@localhost/fitness")

engine = create_engine(
    DATABASE_URL,
    # Remove SQLite-specific connect_args
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()