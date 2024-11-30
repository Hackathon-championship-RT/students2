import logging

from fastapi import APIRouter, Depends, Response, status

from src.bootstrap import Bootstrap
from src.domain.models import ResultData
from src.servises.result_service import InsertResultService, GetAllResultsService, GetUserResultsService, DeleteResultsService
from src.api.result.shemas import ResultSchema

router = APIRouter()


@router.post("/records")
async def new_result(result: ResultData, result_service: InsertResultService = Depends(InsertResultService)):
    await result_service(result_data=result, uow=Bootstrap.bootstraped.uow_partial())
    logging.info(f"New result for {result.username} inserted")
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/records")
async def get_results(limit: int, result_service: GetAllResultsService = Depends(GetAllResultsService)):
    results = await result_service(uow=Bootstrap.bootstraped.uow_partial())
    results.sort(key=lambda r: (-r.level, r.time, r.shuffles))
    results = results[:limit]
    return [ResultSchema.model_validate(result) for result in results]


@router.get("/records/<username>")
async def get_user_results(username: str, result_service: GetUserResultsService = Depends(GetUserResultsService)):
    results = await result_service(username=username, uow=Bootstrap.bootstraped.uow_partial())
    return [ResultSchema.model_validate(result) for result in results]


@router.delete("/records")
async def delete_results(result_service: DeleteResultsService = Depends(DeleteResultsService)):
    await result_service(uow=Bootstrap.bootstraped.uow_partial())
    logging.info("Results are cleared")
