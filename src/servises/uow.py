from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.adapters import SQLAlchemyAdapter
from src.db.repositories import (
    AbstractResultRepository,
    AbstractUserRepository,
    ResultRepository,
    UserRepository,
)


class AbstractUnitOfWork(ABC):
    user_repository: AbstractUserRepository
    result_repository: AbstractResultRepository

    @abstractmethod
    def __aenter__(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def __aexit__(self, *args) -> Any:
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, db_adapter: SQLAlchemyAdapter) -> None:
        self.client_db_adapter = db_adapter
        self.user_repository: AbstractUserRepository
        self.scoreboard_repository: AbstractResultRepository
        self.session: AsyncSession

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self.client_db_adapter.sessionmaker()
        if not self.session:
            raise ValueError("Failed to initialize session")
        self.user_repository = UserRepository(session=self.session)
        self.scoreboard_repository = ResultRepository(session=self.session)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if self.session:
            try:
                if exc_type is None:
                    await self.session.commit()
                else:
                    await self.session.rollback()
            finally:
                await self.session.close()
