from pydantic import BaseModel, SecretStr, ConfigDict, field_validator
from fastapi import HTTPException, status


class BaseUser(BaseModel):
    login: str


class User(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    password: SecretStr


class CreateUser(BaseUser):
    password: str

    @field_validator("login", mode="after")
    @staticmethod
    def check_login(login: str) -> str:
        if login[:5] != "user_":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Логин пользователя обязан начинаться с 'user_'"
            )

        return login
