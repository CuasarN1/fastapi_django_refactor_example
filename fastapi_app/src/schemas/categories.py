from pydantic import BaseModel, Field
from typing import Optional

from schemas.users import User


class CategoryBase(BaseModel):
    title: str = Field(max_length=256)
    description: str
    is_published: bool


class CategoryCreate(CategoryBase):
    author_id: int


class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(max_length=256)
    description: Optional[str]
    is_published: Optional[bool]


class Category(BaseModel):
    id: int
    author: User
    title: str = Field(max_length=256)
    description: str
    is_published: bool
