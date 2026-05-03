from typing import Any

import pytest

from application.domain.user.use_cases.create_user import CreateUserUseCase
from application.core.exceptions.database_exceptions import EntityAlreadyExistsException
from application.core.exceptions.domain_exceptions import UserLoginIsNotUniqueException
from application.schemas.users import CreateUser

from tests.mocks import AsyncCallRecorder, FakeRow


class TestCreateUserUseCase:
    async def test_hashes_password_and_returns_user(
        self, create_user_use_case: CreateUserUseCase
    ) -> None:
        captured: dict[str, CreateUser] = {}

        async def fake_create(session: Any, user: CreateUser) -> FakeRow:
            captured["user"] = user
            return FakeRow(login=user.login, password=user.password)

        create_user_use_case._repo.create = AsyncCallRecorder(side_effect=fake_create)
        payload: CreateUser = CreateUser(login="user_alice", password="plain")

        result: Any = await create_user_use_case.execute(user=payload)

        assert result.login == "user_alice"
        # Password sent to the repo is hashed, not plain
        assert captured["user"].password != "plain"
        assert len(captured["user"].password) > 0

    async def test_raises_when_login_is_duplicate(
        self, create_user_use_case: CreateUserUseCase
    ) -> None:
        create_user_use_case._repo.create = AsyncCallRecorder(
            side_effect=EntityAlreadyExistsException()
        )
        payload: CreateUser = CreateUser(login="user_dup", password="pw")

        with pytest.raises(UserLoginIsNotUniqueException) as exc_info:
            await create_user_use_case.execute(user=payload)

        assert "user_dup" in exc_info.value.get_detail()
