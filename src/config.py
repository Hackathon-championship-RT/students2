import logging
import os

from src import logger


class Config:
    LOGGING_LEVEL: str

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_URL: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    API_VERSION: str
    API_DESCRIPTION: str

    JWT_SECRET: str

    def __init__(self) -> None:
        self.LOGGING_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
        logger.setup_logger(self.LOGGING_LEVEL)

        # Database Config
        try:
            self.DATABASE_HOST: str = os.environ["POSTGRES_HOST"]
            self.DATABASE_PORT: int = int(os.environ["POSTGRES_PORT"])
            self.DATABASE_USER: str = os.environ["POSTGRES_USER"]
            self.DATABASE_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
            self.DATABASE_URL: str = f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/postgres"
        except KeyError:
            logging.exception("Database environment variable(s) not set!")
            raise

        # api
        self.API_VERSION: str = "0.0.1"
        self.API_DESCRIPTION: str = "beautiful api"

        # JWT
        self.JWT_SECRET: str = "spasibo"
