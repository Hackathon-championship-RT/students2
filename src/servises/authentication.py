import logging
from typing import Optional

import jwt

from src.bootstrap import Bootstrap
from src.domain.models import UserData
from src.servises.uow import UnitOfWork


class SignUpService:
    async def __call__(self, user_data: UserData, uow: UnitOfWork) -> None:
        async with uow.start() as uow_session:
            logging.debug("Registring: %s", str(user_data))
            username, password = user_data.username, user_data.password

            await uow_session.users.insert_user(username, password)


class SignInService:
    async def __call__(self, user_data: UserData, uow: UnitOfWork) -> str | bool:
        async with uow.start() as uow_session:
            logging.debug("Sign in: %s", str(user_data))
            username = user_data.username

            result = await uow_session.users.get_user_by_username(username)
            if not result or user_data.password != result.password:
                return False
            token = jwt.encode(
                payload={"name": username},
                key=Bootstrap.bootstraped.config.JWT_SECRET,
                algorithm="HS256",
            )
            await uow_session.users.add_token(username, token)
            logging.debug(token)
            return token


class TokenService:
    async def __call__(self, username: str, uow: UnitOfWork) -> Optional["User"]:
        async with uow.start() as uow_session:
            result = await uow_session.users.get_user_by_username(username)
            return result
