from pydantic import BaseModel


class UserData(BaseModel):
    username: str
    password: str


class ResultData(BaseModel):
    level: int
    score: int
