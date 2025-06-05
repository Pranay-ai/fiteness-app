from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import models , database , routers


@asynccontextmanager
async def lifespan(app: FastAPI):

    models.Base.metadata.create_all(bind=database.engine)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(routers.user_router)
app.include_router(routers.fitnessclass_router)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with SQLite!"}

