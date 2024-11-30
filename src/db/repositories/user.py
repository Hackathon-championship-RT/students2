from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.models import User
from src.api.auth.schemas import UserData


class AbstractUserRepository(ABC):
    @abstractmethod
    async def insert_user(self, username: str, hashed_password: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[UserData]:
        raise NotImplementedError()

    @abstractmethod
    async def get_users(self) -> List[UserData | None]:
        raise NotImplementedError()


class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_user(self, username: str, hashed_password: str) -> None:
        async with self.session as session:
            user = User(username=username, password=hashed_password)
            session.add(user)
            await session.commit()

    async def get_user_by_username(self, username: str) -> Optional[UserData]:
        async with self.session as session:
            result = await session.execute(
                select(User).where(User.username == username)
            )
            db_users = result.unique().scalar_one_or_none()
            return self._to_user_data(db_users)

    async def get_users(self) -> List[UserData | None]:
        async with self.session as session:
            result = await session.execute(select(User))
            db_users = result.unique().scalars().all()
            return [self._to_user_data(user) for user in db_users]

    def _to_user_data(self, db_user: User | None) -> Optional[UserData]:
        if db_user is None:
            return None
        return UserData(
            username=str(db_user.username),
        )
