from pydantic import BaseModel


class ResultSchema(BaseModel):
    id: int
    shuffles: int
    time: int
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True
