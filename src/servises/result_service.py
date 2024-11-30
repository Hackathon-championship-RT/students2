from typing import List

from src.servises.uow import UnitOfWork
from src.domain.models import ResultData


class InsertResultService:
    async def __call__(self, result_data: ResultData, uow: UnitOfWork):
        async with uow.start() as uow_session:
            return await uow_session.results.insert_result(result_data.username, result_data.level, result_data.time, result_data.shuffles)


class GetAllResultsService:
    async def __call__(self, uow: UnitOfWork) -> List["Result"]:
        async with uow.start() as uow_session:
            return await uow_session.results.get_all_results()


class GetUserResultsService:
    async def __call__(self, username: str, uow: UnitOfWork) -> List["Result"]:
        async with uow.start() as uow_session:
            return await uow_session.results.get_user_results(username)


class DeleteResultsService:
    async def __call__(self, uow: UnitOfWork):
        async with uow.start() as uow_session:
            return await uow_session.results.delete_results()
