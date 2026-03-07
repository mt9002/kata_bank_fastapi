from fastapi import APIRouter
from app.modules.account.view import account_router
router = APIRouter()

router.include_router(router=account_router)
