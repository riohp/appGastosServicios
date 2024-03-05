import sys


from appv1.models.Transactions import Transactions
from fastapi import HTTPException
from sqlalchemy.orm import Session
from appv1.schemas.transactions import BaseTransaction, UpdateTransaction, TransactionType, CreateTransaction
from appv1.schemas.users import UserRead



def create_new_transaction(new_transaction: CreateTransaction, db: Session):
    
    if new_transaction.amount < 0:
        raise HTTPException(status_code=400, detail="El monto no puede ser negativo")
    elif new_transaction.amount == 0:
        raise HTTPException(status_code=400, detail="El monto no puede ser cero")
    

    db_transaction = Transactions(
        user_id=new_transaction.user_id,
        category_id=new_transaction.category_id,
        amount=new_transaction.amount,
        t_description=new_transaction.t_description,
        t_date=new_transaction.t_date,
        t_type=new_transaction.t_type
    )

    try:
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear transaccion: {str(e)}")
    

def update_transaction_new(transaction: UpdateTransaction, db: Session, current_user: UserRead):
    db_transaction = get_transaction_by_id(transaction.transactions_id, db)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    # Verificar si la transacción pertenece al usuario actual
    if db_transaction.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar esta transacción")

    # Verificar si el transactions_id pertenece al user_id actual
    if db_transaction.user_id != transaction.user_id:
        raise HTTPException(status_code=403, detail="El transactions_id no pertenece al usuario actual")

    if db_transaction.category_id != transaction.category_id:
        raise HTTPException(status_code=403, detail="El no exite esa categoria masamorrete")
    
    try:
        db_transaction.user_id = transaction.user_id
        db_transaction.category_id = transaction.category_id
        db_transaction.amount = transaction.amount
        db_transaction.t_description = transaction.t_description
        db_transaction.t_date = transaction.t_date
        db_transaction.t_type = transaction.t_type
        
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar transacción: {str(e)}")


        
        
def get_transaction_by_id(transaction_id: int, db: Session):
    transaction = db.query(Transactions).filter(Transactions.transactions_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaccion no encontrada")
    return transaction
        
    
    
    
   