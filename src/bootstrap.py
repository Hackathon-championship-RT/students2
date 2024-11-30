import logging
from dataclasses import dataclass
from typing import Any, Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import Config
from src.servises.uow import UnitOfWork


@dataclass
class Bootstraped:
    config: Config
    fast_api: FastAPI
    uow_partial: Callable[[], UnitOfWork]


class Bootstrap:
    bootstraped: Bootstraped

    def __call__(self, *args: Any, **kwds: Any) -> Bootstraped:
        logging.info("ATTEMPTING SERVICE BOOTSTRAP - loading config")
        config = Config()

        logging.info("BOOTSTRAPPING - UoW")

        def uow_partial() -> UnitOfWork:
            engine = create_async_engine(config.DATABASE_URL)
            session_factory = async_sessionmaker(bind=engine)

            return UnitOfWork(session_factory=session_factory)

        logging.info("BOOTSTRAPING - FASTAPI")
        fast_api = Bootstrap.bootstrap_fastapi(config)

        Bootstrap.bootstraped = Bootstraped(
            fast_api=fast_api,
            config=config,
            uow_partial=uow_partial,
        )

        logging.info("BOOTSTRAPING Completed")

        return Bootstrap.bootstraped

    @staticmethod
    def bootstrap_fastapi(config: Config) -> FastAPI:
        logging.debug("BOOTSTRAPPING - fast api")
        fast_api = FastAPI(
            title=f"AutoMahjong API {config.API_VERSION}",
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

        return fast_api
