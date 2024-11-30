from pydantic import BaseModel


class UserData(BaseModel):
    username: str
    password: str


class ResultData(BaseModel):
    username: str
    level: int
    time: int
    shuffles: int