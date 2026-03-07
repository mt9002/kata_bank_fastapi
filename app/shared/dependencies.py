
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from app.modules.account.repository import AccountRepository, SqlAccountRepository
from app.modules.account.service import AccountService

from app.core.settings import get_session

SessionDep = Annotated[Session, Depends(get_session)]

def get_account_repo(session: SessionDep) -> AccountRepository:
    return SqlAccountRepository(session=session)

def get_account_service(repo: AccountRepository = Depends(get_account_repo)) -> AccountService:
    return AccountService(repo=repo)

AccountRepositoryDep = Annotated[AccountRepository, Depends(get_account_repo)]
AccountServiceDep = Annotated[AccountService, Depends(get_account_service)]



