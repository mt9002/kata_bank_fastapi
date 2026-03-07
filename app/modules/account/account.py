from datetime import datetime
from typing import List, Optional

from app.modules.account.exceptions import InvalidInitialAmountException
from app.modules.account.extract import Extract


class Account:

    def __init__(
        self,
        id: Optional[int] = None,
        num_account: str = None,
        amount: float = 0.0,
        user_identity: str = "",
        extracts: Optional[List] = None,
        register_date: datetime = None
    ):
        self._validate_amount(amount)
        self.id = id
        self.num_account = num_account
        self.amount = amount
        self.user_identity = user_identity
        self.extracts = extracts or []
        self.register_date = register_date

    def assign_num_account(self, num_account: str):
        self.num_account = num_account

    def deposit(self, amount: float):
        self._ensure_positive_amount(amount, "Deposit amount must be positive")
        self.amount += amount
        self.extracts.append(
            Extract(amount=amount, balance=self.amount)
        )

    def withdraw(self, amount: float):
        self._ensure_positive_amount(amount, "Withdraw amount must be positive")
        self._insufficient_funds(amount)
        self.amount -= amount
        self.extracts.append(
            Extract(amount=-amount, balance=self.amount)
        )

    def _insufficient_funds(self, amount: float):
        if amount > self.amount:
            raise ValueError("Insufficient funds")

    def _ensure_positive_amount(self, amount: float, message: str):
        if amount <= 0:
            raise ValueError(message)

    def _validate_amount(self, amount):
        if amount % 10 != 0:
            raise InvalidInitialAmountException("El monto debe terminar en 0")
