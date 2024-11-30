import logging
from dataclasses import dataclass
from time import sleep
from typing import Any, Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from src.api.adapters import SQLAlchemyAdapter
from src.config import Config
from src.servises.uow import AbstractUnitOfWork, UnitOfWork


@dataclass
class Bootstraped:
    sql_db_adapter: SQLAlchemyAdapter
    config: Config
    fast_api: FastAPI
    uow_partial: Callable[[], AbstractUnitOfWork]


class Bootstrap:
    bootstraped: Bootstraped

    def __call__(self, *args: Any, **kwds: Any) -> Bootstraped:
        logging.info("ATTEMPTING SERVICE BOOTSTRAP - loading config")
        config = Config()

        logging.info("BOOTSTRAPING - Postgres")
        db_adapter = SQLAlchemyAdapter(
            config.DATABASE_URL,
            engine_kwargs={"future": True},
        )

        logging.info("BOOTSTRAPPING - UoW")

        def uow_partial() -> UnitOfWork:
            return UnitOfWork(db_adapter)

        logging.info("BOOTSTRAPING - FASTAPI")
        fast_api = Bootstrap.bootstrap_fastapi(config, db_adapter)

        Bootstrap.bootstraped = Bootstraped(
            sql_db_adapter=db_adapter,
            fast_api=fast_api,
            config=config,
            uow_partial=uow_partial,
        )

        logging.info("BOOTSTRAPING Completed")

        return Bootstrap.bootstraped

    @staticmethod
    def bootstrap_fastapi(config: Config, db_adapter: SQLAlchemyAdapter) -> FastAPI:
        logging.debug("BOOTSTRAPPING - fast api")
        fast_api = FastAPI(
            title=f"AutoMahjong {config.API_VERSION}",
            description=config.API_DESCRIPTION,
            root_path="/api",
            docs_url="/docs",
            openapi_url="/openapi.json",
        )

        fast_api.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=["*"],
            allow_methods=["GET", "POST"],
            allow_headers=["*"],
        )

        @fast_api.on_event("startup")
        async def startup() -> None:
            connected = False
            while not connected:
                try:
                    async with db_adapter.connect() as conn:
                        await conn.execute(text("SELECT 1"))
                    connected = True
                except Exception as e:
                    logging.error(f"Unable to connect to DB - Retrying... {e}")
                    sleep(3)

        @fast_api.on_event("shutdown")
        async def shutdown() -> None:
            await db_adapter.close()

        return fast_api
