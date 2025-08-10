from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.settings import settings

engine: AsyncEngine | None = None
SessionLocal: sessionmaker | None = None

def init_engine() -> None:
    global engine, SessionLocal
    engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)
    SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def dispose_engine() -> None:
    if engine is not None:
        await engine.dispose()

async def get_session() -> AsyncSession:
    assert SessionLocal is not None, "DB engine is not initialized"
    async with SessionLocal() as session:
        yield session

class Base(DeclarativeBase):
    pass