from typing import List

from src.servises.uow import AbstractUnitOfWork


class GetUsers:
    async def __call__(self, uow: AbstractUnitOfWork) -> List["User"]:
        async with uow:
            return await uow.user_repository.get_users()
