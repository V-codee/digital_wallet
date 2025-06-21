from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database, auth, schemas

router = APIRouter()

get_db = database.get_db

#all my purchases
@router.get("/my-purchases", response_model=list[schemas.Product])
def get_my_purchases(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    purchases = db.query(models.Purchase).filter(models.Purchase.user_id == current_user.id).all()
    products = [purchase.product for purchase in purchases]
    return products

#Purchase a product
@router.post("/purchase")
def purchase_product(
    request: schemas.PurchaseRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    product = db.query(models.Product).filter(models.Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if current_user.wallet.balance < product.price:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    #Deduct price from user's wallet
    current_user.wallet.balance -= product.price

    #Log the transaction
    transaction = models.Transaction(
        user_id=current_user.id,
        kind="purchase",
        amount=product.price,
        updated_balance=current_user.wallet.balance
    )
    db.add(transaction)

    #Create purchase record
    purchase = models.Purchase(user_id=current_user.id, product_id=product.id)
    db.add(purchase)

    db.commit()
    return {"msg": "Product purchased successfully"}
