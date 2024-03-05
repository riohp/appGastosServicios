from datetime import date
from pydantic import BaseModel 
from enum import Enum as pydanticEnum

class TransactionType(str, pydanticEnum):
    revenue = 'revenue'
    expenses = 'expenses'

class BaseTransaction(BaseModel):
    user_id: str
    category_id: int
    amount: float
    t_description: str
    t_type: TransactionType
    t_date: date

class CreateTransaction(BaseTransaction):
    pass

class UpdateTransaction(BaseTransaction):
    transactions_id: int    

    
    
