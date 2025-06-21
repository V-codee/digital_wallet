from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, database, auth
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

get_db = database.get_db

#Registration Route
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth.register_user(user, db)

#Login Route
@router.post("/login")
#login by email
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     user = auth.authenticate_user(form_data.email, form_data.password, db)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
    
#     access_token = auth.create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}

#login by username
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
