import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app import models, schemas, database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


# Constants
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

#Password hashing algo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#DB dependency to access db
get_db = database.get_db

#Password hashing
def hash_password(password: str):
    return pwd_context.hash(password)
#Password verification
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#JWT token creation
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "sub": data.get("sub")})  # sub stores user identity
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#User registration
def register_user(user: schemas.UserCreate, db: Session):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    #Create wallet with 0.0 balance for any new user
    new_wallet = models.Wallet(user_id=new_user.id, balance=0.0)
    db.add(new_wallet)
    db.commit()
    
    return new_user

#User authentication (login via email)
# def authenticate_user(email: str, password: str, db: Session):
#     user = db.query(models.User).filter(models.User.email == email).first()
#     if not user or not verify_password(password, user.hashed_password):
#         return None
#     return user

#User authentication (via uesername)
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

#To get current logged-in User from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #email = payload.get("sub")  #if we use email
        username: str = payload.get("sub")   
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    #user = db.query(models.User).filter(models.User.email == email).first()    #if we use email
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

