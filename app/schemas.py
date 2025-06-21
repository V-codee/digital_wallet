from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

#User registration
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

#User response 
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

#Login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#Wallet schema
class Wallet(BaseModel):
    id: int
    balance: float

    class Config:
        from_attributes = True

#Deposit schema
class Deposit(BaseModel):
    amount: float

#Product list
class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True

#Product schema
class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

    class Config:
        orm_mode = True

#Purchase schema
class PurchaseRequest(BaseModel):
    product_id: int

class Transaction(BaseModel):
    id: int
    kind: str
    amount: float
    updated_balance: float
    timestamp: datetime

    class Config:
        orm_mode = True

#transfer money
class TransferRequest(BaseModel):
    recipient_username: str
    amount: float