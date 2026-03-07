from fastapi import FastAPI
from app.core.settings import settings
from app.shared.handler_exception import register_exception_handlers
from app.shared.routes import router
app = FastAPI(
    title='kata_bank_fastapi',
    description=''
)
app.include_router(router=router, prefix=settings.API_V1_STR)
register_exception_handlers(app)
