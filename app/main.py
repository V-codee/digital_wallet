from fastapi import FastAPI
from app import models, database
from app.routes import user, wallet, transactions, purchase, protected, product

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

#the router
app.include_router(user.router)
app.include_router(wallet.router)
app.include_router(transactions.router)
app.include_router(purchase.router)
app.include_router(protected.router)
app.include_router(product.router)