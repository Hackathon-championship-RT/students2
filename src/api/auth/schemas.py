from typing import List, Optional

from pydantic import BaseModel

from src.api.result.shemas import ResultSchema


class UserSchema(BaseModel):
    id: int
    username: str
    results: Optional[List[ResultSchema]] = None

    class Config:
        orm_mode = True
        from_attributes = True
