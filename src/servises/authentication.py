import logging
from typing import Optional

from src.domain.models import UserData
from src.servises.uow import UnitOfWork


class SignUpService:
    async def __call__(self, user_data: UserData, uow: UnitOfWork) -> None:
        async with uow:
            logging.debug("Registring: %s", str(user_data))
            username, password = user_data.username, user_data.password

            await uow.user_repository.insert_user(username, password)


class SignInService:
    async def __call__(self, user_data: UserData, uow: UnitOfWork) -> Optional["User"]:
        async with uow:
            logging.debug("Sign in: %s", str(user_data))
            username = user_data.username

            return await uow.user_repository.get_user_by_username(username)


class GetUser:
    async def __call__(self, username: str, uow: UnitOfWork):
        async with uow:
            result = await uow.user_repository.get_user_by_username(username)
            return result
