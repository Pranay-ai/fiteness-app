# routers/__init__.py
from .user_router import router as user_router
from .class_router import router as fitnessclass_router
from .booking_router import router as booking_router

__all__ = ["user_router" , "fitnessclass_router" ,"booking_router"]