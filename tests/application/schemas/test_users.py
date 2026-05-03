import pytest
from fastapi import HTTPException
from pydantic import SecretStr

from application.schemas.users import BaseUser, CreateUser, User


class TestCreateUser:
    def test_login_with_user_prefix_passes(self) -> None:
        user: CreateUser = CreateUser(login="user_alice", password="secret")
        assert user.login == "user_alice"
        assert user.password == "secret"

    def test_login_exactly_user_prefix_is_accepted(self) -> None:
        user: CreateUser = CreateUser(login="user_", password="x")
        assert user.login == "user_"

    def test_login_without_user_prefix_raises_http_422(self) -> None:
        with pytest.raises(HTTPException) as exc_info:
            CreateUser(login="alice", password="secret")
        assert exc_info.value.status_code == 422
        assert "user_" in exc_info.value.detail

    def test_short_login_without_prefix_raises(self) -> None:
        with pytest.raises(HTTPException):
            CreateUser(login="abc", password="secret")


class TestUser:
    def test_password_is_secret_str(self) -> None:
        user: User = User(login="user_x", password=SecretStr("h"))
        # SecretStr hides the value in repr
        assert "h" not in repr(user)

    def test_can_be_built_from_attributes(self) -> None:
        class Obj:
            login: str = "user_x"
            password: str = "h"

        user: User = User.model_validate(Obj())
        assert user.login == "user_x"


class TestBaseUser:
    def test_only_requires_login(self) -> None:
        base: BaseUser = BaseUser(login="anything")
        assert base.login == "anything"
