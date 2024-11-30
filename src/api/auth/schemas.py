from typing import List, Optional

from pydantic import BaseModel

from src.api.result.shemas import ResultSchema


class UserSchema(BaseModel):
    id: int
    username: str
    results: Optional[List[ResultSchema]] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserData(BaseModel):
    username: str
