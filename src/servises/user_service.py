from typing import List

from src.servises.uow import UnitOfWork


class GetUsers:
    async def __call__(self, uow: UnitOfWork) -> List["User"]:
        async with uow.start() as uow_session:
            return await uow_session.users.get_users()
