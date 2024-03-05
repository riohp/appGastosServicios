from typing import List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from core.token import get_current_user
from db.session import get_session
from appv1.schemas.transactions import  TransactionType, BaseTransaction, UpdateTransaction, CreateTransaction
from appv1.schemas.users import UserRead
from appv1.models.Transactions import Transactions
from appv1.crud.transactions import create_new_transaction, update_transaction_new



router = APIRouter()



@router.post("/create-transaction/", response_model=CreateTransaction)
async def create_transaction(
    transaction: CreateTransaction, 
    db: Session = Depends(get_session), 
    current_user: UserRead = Depends(get_current_user)
):
    if current_user.user_role == 'user' and current_user.user_id == transaction.user_id:
        return create_new_transaction(transaction, db)
    raise HTTPException(status_code=401, detail="Not authorized")


    
@router.put("/update-transaction/", response_model=UpdateTransaction)
def update_transaction(
    transaction: UpdateTransaction, 
    db: Session = Depends(get_session), 
    current_user: UserRead = Depends(get_current_user)
):
    if current_user.user_role == "user":
        if transaction is not None: 
            transaction_updated = update_transaction_new(transaction, db, current_user)
            if transaction_updated is None:
                raise HTTPException(status_code=404, detail="Transacción no encontrada")
            return transaction_updated
        else:
            raise HTTPException(status_code=400, detail="Los datos de la transacción no pueden estar vacíos")
    raise HTTPException(status_code=401, detail="Token inválido")


@router.get("/get-all-transactions/", response_model=List[BaseTransaction])
def get_all_transactions(db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        return db.query(Transactions).all()
    elif current_user.user_role == "user":
        return db.query(Transactions).filter(Transactions.user_id == current_user.user_id).all()
    raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/get-transaction/{transaction_id}", response_model=BaseTransaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    # Obtener la transacción por su ID
    transaction = db.query(Transactions).filter(Transactions.transactions_id == transaction_id).first()

 
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    if current_user.user_role == "admin" or (current_user.user_role == "user" and transaction.user_id == current_user.user_id):
        return transaction

    raise HTTPException(status_code=403, detail="No tienes permiso para acceder a esta transacción")










