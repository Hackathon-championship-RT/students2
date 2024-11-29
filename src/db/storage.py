from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class SQLAlchemyStorage:
    engine: Engine
    sessionmaker: sessionmaker

    def __init__(self, engine: Engine):
        self.engine = engine
        self.sessionmaker = sessionmaker(bind=self.engine, expire_on_commit=False)

    @classmethod
    def from_url(cls, url: str):
        engine = create_engine(url)
        return cls(engine)

    def create_session(self) -> Session:
        return self.sessionmaker()

    def close_connection(self):
        self.engine.dispose()


storage: SQLAlchemyStorage
