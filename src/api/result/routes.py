import logging

from fastapi import APIRouter, Depends, Response, status

from src.api.auth.auth import get_current_user
from src.api.result.shemas import ResultSchema
from src.bootstrap import Bootstrap
from src.db.models import User
from src.domain.models import ResultData
from src.servises.result_service import (
    DeleteResultsService,
    GetAllResultsService,
    GetUserResultsService,
    InsertResultService,
)

router = APIRouter()


@router.post("/records")
async def new_result(
    result: ResultData,
    result_service: InsertResultService = Depends(InsertResultService),
    user: User = Depends(get_current_user),
):
    await result_service(result_data=result, username=user.username, uow=Bootstrap.bootstraped.uow_partial())
    logging.info(f"New result for {user.username} inserted")
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/records")
async def get_results(
    limit: int, result_service: GetAllResultsService = Depends(GetAllResultsService)
):
    results = await result_service(uow=Bootstrap.bootstraped.uow_partial())

    for result in results:
        result.username = result.user.username

    results = sorted(results, key=lambda r: (-r.level, -r.score))[:limit]
    return [ResultSchema.model_validate(result) for result in results]


@router.get("/records/<username>")
async def get_user_results(
    username: str,
    result_service: GetUserResultsService = Depends(GetUserResultsService),
):
    results = await result_service(
        username=username, uow=Bootstrap.bootstraped.uow_partial()
    )
    return [ResultSchema.model_validate(result) for result in results]


@router.delete("/records")
async def delete_results(
    result_service: DeleteResultsService = Depends(DeleteResultsService),
):
    await result_service(uow=Bootstrap.bootstraped.uow_partial())
    logging.info("Results are cleared")
