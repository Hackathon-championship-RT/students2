from typing import List

from src.domain.models import ResultData
from src.servises.uow import AbstractUnitOfWork


class InsertResultService:
    async def __call__(self, result_data: ResultData, uow: AbstractUnitOfWork):
        async with uow:
            return await uow.result_repository.insert_result(
                result_data.username,
                result_data.level,
                result_data.score,
            )


class GetAllResultsService:
    async def __call__(self, uow: AbstractUnitOfWork) -> List["Result"]:
        async with uow:
            return await uow.result_repository.get_all_results()


class GetUserResultsService:
    async def __call__(self, username: str, uow: AbstractUnitOfWork) -> List["Result"]:
        async with uow:
            return await uow.result_repository.get_user_results(username)


class DeleteResultsService:
    async def __call__(self, uow: AbstractUnitOfWork):
        async with uow:
            return await uow.result_repository.delete_results()
