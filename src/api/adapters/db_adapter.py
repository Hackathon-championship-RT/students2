import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.exceptions import SQLalchemyEngineError


class SQLAlchemyAdapter:
    def __init__(self, host: str, engine_kwargs: dict[str, Any]) -> None:
        self._engine = create_async_engine(host, **engine_kwargs)
        self.sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise SQLalchemyEngineError("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self.sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise SQLalchemyEngineError("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.sessionmaker is None:
            raise SQLalchemyEngineError("DatabaseSessionManager is not initialized")

        session = self.sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
