from pydantic import BaseModel, SecretStr, datetime
from typing import Optional


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: SecretStr


class UserUpdate(BaseModel):
    login: Optional[str]
    password: Optional[SecretStr]


class User(UserBase):
    id: int
    created_at: datetime
