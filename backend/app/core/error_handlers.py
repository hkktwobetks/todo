from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .exceptions import NotFoundError
from app.shared.exceptions import AppError
import logging
logger = logging.getLogger(__name__)

# 422: バリデーションエラー
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "detail": exc.errors()
        }
    )

# 404: リソースが見つからない
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "not_found",
            "detail": exc.detail
        }
    )

async def handle_app_error(_: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.code, "detail": exc.detail},
    )

async def handle_request_validation(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "validation_error", "detail": exc.errors()},
    )

async def handle_unexpected(_: Request, exc: Exception):
    # サーバ側には詳細ログ、クライアントには安全なメッセージ
    logger.exception("unexpected error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": "unexpected error"},
    )
