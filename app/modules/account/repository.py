
from abc import ABC, abstractmethod
from typing import Any


from sqlalchemy.orm import Session, joinedload

from app.modules.account.account import Account
from app.modules.account.mapper import BaseMapper
from app.modules.account.models import AccountModel


class AccountRepository(ABC):

    @abstractmethod
    def find_by_num_account(self, num_account: str) -> Account | None:
        pass

    @abstractmethod
    def find_by_user_identity(self, user_identity: str) -> Account | None:
        pass

    @abstractmethod
    def save(self, account: Account) -> Account:
        pass


class SqlAccountRepository(AccountRepository):

    def __init__(self, session: Session):
        self.session = session

    def find_by_num_account(self, num_account: str) -> Account | None:
        model: Any | None = (
            self.session.query(AccountModel)
            .options(joinedload(AccountModel.extracts))
            .filter(AccountModel.num_account == num_account)
            .first()
        )
        return BaseMapper.to_domain(model)

    def find_by_user_identity(self, user_identity: str) -> Account | None:
        model: Any | None = (
            self.session.query(AccountModel)
            .filter(AccountModel.user_identity == user_identity)
            .first()
        )
        return BaseMapper.to_domain(model)

    def save(self, account: Account) -> Account:
        model = BaseMapper.to_model(account)

        model = self.session.merge(model)
        self.session.commit()
        self.session.refresh(model)

        return BaseMapper.to_domain(model)