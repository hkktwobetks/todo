from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import init_engine, dispose_engine
from app.domains.tasks import router as task_router
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.shared.exceptions import AppError
from app.core.error_handlers import validation_exception_handler, not_found_exception_handler
from app.core.exceptions import NotFoundError
from app.core.error_handlers import handle_app_error, handle_request_validation
from app.core.error_handlers import handle_unexpected
from app.core.logging import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_engine()
    # ここで将来: 監視/APM/外部クライアント初期化など
    try:
        yield
    finally:
        await dispose_engine()

app = FastAPI(lifespan=lifespan)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(AppError, handle_app_error)
app.add_exception_handler(RequestValidationError, handle_request_validation)
app.add_exception_handler(Exception, handle_unexpected)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    return {"ok": True}

app.include_router(task_router.router)

# 例外 → 統一JSONに変換
@app.exception_handler(AppError)
async def handle_app_error(_: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.code, "detail": exc.detail},
    )

# Pydantic / FastAPI のバリデーション 422 を整形
@app.exception_handler(RequestValidationError)
async def handle_request_validation(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "validation_error", "detail": exc.errors()},
    )

# “想定外”エラーは 500 にまとめる（ログは後で）
@app.exception_handler(Exception)
async def handle_unexpected(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": "unexpected error"},
    )

