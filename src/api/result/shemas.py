from pydantic import BaseModel


class ResultSchema(BaseModel):
    id: int
    level: int
    score: int
    user_id: int
    username: str

    class Config:
        from_attributes = True
