from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.user import UserRepository
from src.db.repositories.result import ResultRepository


class AbstractUnitOfWork(ABC):
    @abstractmethod
    @asynccontextmanager
    def start(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def users(self):
        raise NotImplementedError()


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session: AsyncSession | None = None

    @asynccontextmanager
    async def start(self):
        self._session = self.session_factory()
        try:
            yield self
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise
        finally:
            await self._session.close()

    @property
    def users(self) -> UserRepository:
        if not self._session:
            raise RuntimeError("UnitOfWork must be started before accessing repositories.")
        return UserRepository(self._session)

    @property
    def results(self) -> ResultRepository:
        if not self._session:
            raise RuntimeError("UnitOfWork must be started before accessing repositories.")
        return ResultRepository(self._session)
