from pydantic import BaseModel


class ResultSchema(BaseModel):
    id: int
    shuffles: int
    time: int
    user_id: int

    class Config:
        from_attributes = True
