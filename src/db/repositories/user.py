from typing import List

from sqlalchemy.orm import Session

from src.db.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    async def insert_user(self, username: str, hashed_password: str) -> None:
        with self.session as session:
            user = User()
            user.username = username
            user.password = hashed_password
            session.add(user)
            session.commit()

    async def get_userdata_by_username(self, username) -> User | None:
        with self.session as session:
            user = session.query(User).filter_by(username=username).first()
        return user

    async def get_users(self) -> List[User]:
        with self.session as session:
            users = session.query(User).all()
        return users

    async def add_token(self, username, token) -> None:
        with self.session as session:
            user = await self.get_userdata_by_username(username)
            if not user:
                raise ValueError(f"User with username {username} not found.")

            user.token = token
            session.commit()
