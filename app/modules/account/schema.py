from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel

class AccountRequest(BaseModel):
    amount: float
    branch: str
    type_account: str
    user_identity: str

class ExtractResponse(BaseModel):
    amount: float
    balance: float
    account_id: int
    register_date: datetime

    class Config:
        from_attributes = True

class AccountResponse(BaseModel):
    num_account: str
    amount: float
    user_identity: str
    extracts: Optional[List[ExtractResponse]] = None
    register_date: datetime

    class Config:
        from_attributes = True

class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class TransactionRequest(BaseModel):
    num_account: str
    amount: float
    transaction_type: TransactionType

    class Config:
        from_attributes =  True