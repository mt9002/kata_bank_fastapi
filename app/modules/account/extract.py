from datetime import datetime
from typing import Optional


class Extract:
    def __init__(
        self,
        id: Optional[int] = None,
        amount: float = 0,
        balance: float = 0,
        account_id: Optional[int] = None,
        register_date: Optional[datetime] = None
    ):
        self.id = id
        self.amount = amount
        self.balance = balance
        self.account_id = account_id
        self.register_date = register_date