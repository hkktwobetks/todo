# tests/conftest.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ★ テストDB URL（async/asyncpg と sync/psycopg2 を両方用意）
TEST_DB_ASYNC = "postgresql+asyncpg://localhost:5432/todo_db_test"
TEST_DB_SYNC  = "postgresql://localhost:5432/todo_db_test"

# ★ アプリ起動より前に上書き：FastAPIのSettings(.envより優先)に効く
os.environ["DATABASE_URL"] = TEST_DB_ASYNC

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from asgi_lifespan import LifespanManager

# ★ Alembic をテストDBに対して実行（スキーマ最新化）
from alembic import command
from alembic.config import Config as AlembicConfig

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    cfg = AlembicConfig("alembic.ini")
    # iniのsqlalchemy.urlをテストDB(同期URL)に差し替え
    cfg.set_main_option("sqlalchemy.url", TEST_DB_SYNC)
    command.upgrade(cfg, "head")
    yield
    # 必要なら後片付け（任意）
    # command.downgrade(cfg, "base")

import app.core.db as db
from app.main import app

@pytest.fixture
async def client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app, raise_app_exceptions=False)  # ★これ
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c

@pytest.fixture(autouse=True)
async def clean_db(client):  # client 依存＝lifespan後に実行
    assert db.engine is not None
    async with db.engine.begin() as conn:
        await conn.execute(text("DELETE FROM tasks;"))
        await conn.execute(text("ALTER SEQUENCE tasks_id_seq RESTART WITH 1;"))

