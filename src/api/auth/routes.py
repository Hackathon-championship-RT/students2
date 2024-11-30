from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.auth.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
)
from src.api.auth.schemas import Token
from src.api.auth.schemas import UserData as User
from src.bootstrap import Bootstrap
from src.domain.models import UserData
from src.servises.authentication import SignInService, SignUpService
from src.servises.user_service import GetUsers

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
    user_data: UserData, authenticate_user: SignInService = Depends(SignInService)
):
    user = await authenticate_user(user_data, Bootstrap.bootstraped.uow_partial())
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/users")
async def users(
    users_service: GetUsers = Depends(GetUsers),
    user: User = Depends(get_current_user),
):
    return await users_service(uow=Bootstrap.bootstraped.uow_partial())
