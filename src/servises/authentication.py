import logging
from typing import Optional, List

from src.domain.models import UserData


from src.servises.uow import AbstractUnitOfWork, UnitOfWork


class SignUpService:
    async def __call__(self, user_data: UserData, uow: AbstractUnitOfWork) -> None:
        async with uow:
            logging.debug("Registring: %s", str(user_data))
            username, password = user_data.username, user_data.password

            await uow.user_repository.insert_user(username, password)


class SignInService:
    async def __call__(
        self, user_data: UserData, uow: AbstractUnitOfWork
    ) -> Optional[UserData]:
        async with uow:
            logging.debug("Sign in: %s", str(user_data))
            username = user_data.username

            return await uow.user_repository.get_user_by_username(username)


class GetUser:
    async def __call__(self, username: str, uow: AbstractUnitOfWork):
        async with uow:
            result = await uow.user_repository.get_user_by_username(username)
            return result
