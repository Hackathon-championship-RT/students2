import logging
import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

from src.api.auth.schemas import TokenData
from src.api.auth.schemas import UserData
from src.bootstrap import Bootstrap
from src.servises.authentication import GetUser

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
JWT_SECRET = os.getenv("JWT_SECRET")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    authorization_header: str = Security(
        APIKeyHeader(name="Authorization", auto_error=False)
    ),
    get_user: GetUser = Depends(GetUser),
) -> UserData:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not authorization_header:
        raise credentials_exception

    logging.info(authorization_header)

    token = authorization_header.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await get_user(token_data.username, Bootstrap.bootstraped.uow_partial())
    if user is None:
        raise credentials_exception
    return user
