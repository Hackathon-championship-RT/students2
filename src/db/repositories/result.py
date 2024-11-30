from typing import List

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.db.models import Result, User


class ResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_result(self, username: str, level: int, time: int, shuffles: int) -> None:
        async with self.session as session:
            result = await session.execute(select(User).where(User.username == username))
            user = result.unique().scalar_one_or_none()

            if not user:
                raise ValueError(f"User with username '{username}' does not exist.")

            new_result = Result(level=level, time=time, shuffles=shuffles, user=user)
            session.add(new_result)
            await session.commit()

    async def get_all_results(self) -> List[Result]:
        async with self.session as session:
            result = await session.execute(select(Result).options(selectinload(Result.user)))
            return result.unique().scalars().all()

    async def get_user_results(self, username: str) -> List[Result]:
        async with self.session as session:
            query = (
                select(Result)
                .join(User)
                .where(User.username == username)
                .options(selectinload(Result.user))
            )
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def delete_results(self) -> None:
        async with self.session as session:
            query = (
                delete(Result)
            )
            await session.execute(query)
            await session.commit()
