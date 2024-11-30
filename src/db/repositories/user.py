from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.models import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def insert_user(self, username: str, hashed_password: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_users(self) -> List[User]:
        raise NotImplementedError()


class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_user(self, username: str, hashed_password: str) -> None:
        async with self.session as session:
            user = User(username=username, password=hashed_password)
            session.add(user)
            await session.commit()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        async with self.session as session:
            result = await session.execute(
                select(User).where(User.username == username)
            )
            return result.unique().scalar_one_or_none()

    async def get_users(self) -> List[User]:
        async with self.session as session:
            result = await session.execute(select(User))
            return result.unique().scalars().all()
