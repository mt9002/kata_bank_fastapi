from fastapi import APIRouter
from starlette import status
from starlette.responses import StreamingResponse

from app.shared.dependencies import AccountServiceDep
from app.modules.account.schema import AccountResponse, AccountRequest, TransactionRequest

account_router = APIRouter(prefix='/account', tags=['Account'])


@account_router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def post(account_request: AccountRequest, account_service: AccountServiceDep):
    print(account_request.amount)
    return account_service.create_account(account_request)


@account_router.get("/", response_model=AccountResponse)
def get(num_account: str, account_service: AccountServiceDep):
    return account_service.find_by_num_account(num_account)


@account_router.get("/{num_account}/statement_report")
def post(num_account: str, account_service: AccountServiceDep):
    pdf =  account_service.statement(num_account)
    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=extract.pdf"}
    )


@account_router.post("/transaction", status_code=status.HTTP_201_CREATED)
def pos(request: TransactionRequest, account_service: AccountServiceDep):
    return account_service.transaction(request)
