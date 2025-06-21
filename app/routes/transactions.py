from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, database, auth, schemas

router = APIRouter()

get_db = database.get_db

#Get all transactions of the current user
@router.get("/transactions", response_model=list[schemas.Transaction])
def get_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()
    return transactions
