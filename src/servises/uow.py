from abc import ABC, abstractmethod
from contextlib import contextmanager

from src.db.repositories.user import UserRepository


class AbstractUnitOfWork(ABC):
    @abstractmethod
    @contextmanager
    def start(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def users(self):
        raise NotImplementedError()


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session = None

    @contextmanager
    def start(self):
        self._session = self.session_factory()
        try:
            yield self
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        finally:
            self._session.close()

    @property
    def users(self) -> UserRepository:
        return UserRepository(self._session)
