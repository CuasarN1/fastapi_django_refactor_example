from pydantic import BaseModel, Field

from schemas.users import User


class Post(BaseModel):
    author: User
    text: str = Field(max_length=10)
