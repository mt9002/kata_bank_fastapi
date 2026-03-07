from app.modules.account.account import Account
from app.modules.account.extract import Extract
from app.modules.account.models import *


class BaseMapper:

    @staticmethod
    def to_domain(model: AccountModel):
        if model is None:
            return None

        extracts = [
            Extract(
                id=e.id,
                amount=e.amount,
                balance=e.balance,
                account_id=e.account_id,
                register_date=e.register_date
            )
            for e in model.extracts
        ]

        return Account(
            id=model.id,
            num_account=model.num_account,
            extracts=extracts,
            user_identity=model.user_identity,
            amount=model.amount,
            register_date=model.register_date
        )

    @staticmethod
    def to_model(account: Account):
        if account is None:
            return None

        extracts = [
            ExtractModel(
                id=e.id,
                amount=e.amount,
                balance=e.balance,
                account_id=account.id,
                register_date=e.register_date
            )
            for e in account.extracts
        ]
        return AccountModel(
            id=account.id,
            num_account=account.num_account,
            extracts=extracts,
            user_identity=account.user_identity,
            amount=account.amount,
            register_date=account.register_date
        )

