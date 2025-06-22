from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Wallet, Transaction
from app.auth import get_current_user
from app.schemas import Deposit
from datetime import datetime
from app import models, schemas
import httpx
import os
from dotenv import load_dotenv

router = APIRouter(prefix="/wallet",tags=["Wallet"])

load_dotenv()
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

#Get wallet balance
@router.get("/balance")
def get_wallet_balance(
    currency: str = Query(default="INR"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    balance = wallet.balance
    currency = currency.upper()

    if currency != "INR":
        #Call currencyapi.com
        url = f"https://api.currencyapi.com/v3/latest?apikey={CURRENCY_API_KEY}&currencies={currency}&base_currency=INR"
        try:
            response = httpx.get(url)
            data = response.json()
            if currency in data["data"]:
                rate = data["data"][currency]["value"]
                converted = round(balance * rate, 2)
                return {"balance": converted, "currency": currency}
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported currency: {currency}")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Currency conversion failed")

    return {"balance": round(balance, 2), "currency": "INR"}

#Deposit money
@router.post("/deposit")
def deposit_money(deposit: Deposit, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if deposit.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit must be greater than 0")

    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found. Please contact support.")
    else:
        wallet.balance += deposit.amount

    #Add transaction
    transaction = Transaction(
        user_id=current_user.id,
        kind="deposit",
        amount=deposit.amount,
        updated_balance=wallet.balance,
        timestamp=datetime.utcnow()
    )
    db.add(transaction)
    db.commit()
    db.refresh(wallet)

    return {"message": "Deposit successful", "balance": wallet.balance}


#Transfer funds to another user
@router.post("/transfer")
def transfer_funds(
    transfer: schemas.TransferRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    sender_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if not sender_wallet or sender_wallet.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    recipient = db.query(models.User).filter(models.User.username == transfer.recipient_username).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient user not found")

    recipient_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == recipient.id).first()
    if not recipient_wallet:
        raise HTTPException(status_code=404, detail="Recipient wallet not found")

    #Transfer money
    sender_wallet.balance -= transfer.amount
    recipient_wallet.balance += transfer.amount

    #Record transactions for both users
    db.add_all([
        models.Transaction(user_id=current_user.id, kind="payment", amount=transfer.amount, updated_balance=sender_wallet.balance),
        models.Transaction(user_id=recipient.id, kind="deposit", amount=transfer.amount, updated_balance=recipient_wallet.balance)
    ])
    db.commit()

    return {"message": f"₹{transfer.amount} sent to {transfer.recipient_username} successfully."}
