import logging

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Security, Response, status
from fastapi.security import APIKeyHeader

from src.bootstrap import Bootstrap
from src.domain.models import UserData
from src.servises.authentication import SignInService, SignUpService, TokenService
from src.servises.user_service import GetUsers
from src.api.auth.schemas import UserSchema

router = APIRouter()


@router.post("/signup")
async def signup(
    user_data: UserData, auth_service: SignUpService = Depends(SignUpService)
):
    await auth_service(user_data=user_data, uow=Bootstrap.bootstraped.uow_partial())
    return Response(
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/signin")
async def signin(
    user_data: UserData, auth_service: SignInService = Depends(SignInService)
):
    logging.info("sign in")
    status = await auth_service(
        user_data=user_data, uow=Bootstrap.bootstraped.uow_partial()
    )

    if not status:
        logging.info("user %s has not loged in", user_data.username)
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    logging.info("user %s has loged in", user_data.username)
    return Response(
        status_code=200,
    )


@router.get("/users")
async def users(users_service: GetUsers = Depends(GetUsers)):
    users = await users_service(uow=Bootstrap.bootstraped.uow_partial())
    return [UserSchema.model_validate(user) for user in users]


async def check_access_token(
    request: Request,
    authorization_header: str = Security(
        APIKeyHeader(name="Authorization", auto_error=False)
    ),
    token_service: TokenService = Depends(TokenService),
) -> str:
    # Проверяем, что токен передан
    if authorization_header is None:
        raise HTTPException()

    # Проверяем токен на соответствие форме
    if "Bearer " not in authorization_header:
        raise HTTPException()

    # Убираем лишнее из токена
    clear_token = authorization_header.replace("Bearer ", "")

    try:
        # Проверяем валидность токена
        payload = jwt.decode(
            jwt=clear_token,
            key=Bootstrap.bootstraped.config.JWT_SECRET,
            algorithms=["HS256", "RS256"],
        )
    except jwt.InvalidTokenError:
        # В случае невалидности возвращаем ошибку
        raise HTTPException()

    # Идентифицируем пользователя
    user = await token_service(payload["name"])
    if not user:
        raise HTTPException()

    request.state.user = user

    return authorization_header
