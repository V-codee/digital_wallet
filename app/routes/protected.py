from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import UserOut as UserSchema

router = APIRouter(prefix="/protected",tags=["Protected"])

@router.get("/profile", response_model=UserSchema)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
