from typing import Any

import pytest

from application.domain.auth.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from application.core.exceptions.database_exceptions import EntityNotFoundException
from application.core.exceptions.domain_exceptions import (
    UserNotFoundByLoginException,
    WrongPasswordException,
)
from application.resources.auth import get_password_hash

from tests.mocks import AsyncCallRecorder, FakeRow


class TestAuthenticateUserUseCase:
    async def test_returns_user_when_credentials_are_valid(
        self, authenticate_user_use_case: AuthenticateUserUseCase
    ) -> None:
        hashed: str = get_password_hash("correct-password")
        db_user: FakeRow = FakeRow(login="user_alice", password=hashed)
        authenticate_user_use_case._repo.get = AsyncCallRecorder(return_value=db_user)

        result: Any = await authenticate_user_use_case.execute(
            login="user_alice", password="correct-password"
        )

        assert result.login == "user_alice"
        authenticate_user_use_case._repo.get.assert_awaited_once()

    async def test_raises_when_user_not_found(
        self, authenticate_user_use_case: AuthenticateUserUseCase
    ) -> None:
        authenticate_user_use_case._repo.get = AsyncCallRecorder(
            side_effect=EntityNotFoundException()
        )

        with pytest.raises(UserNotFoundByLoginException) as exc_info:
            await authenticate_user_use_case.execute(login="missing", password="x")

        assert "missing" in exc_info.value.get_detail()

    async def test_raises_when_password_is_wrong(
        self, authenticate_user_use_case: AuthenticateUserUseCase
    ) -> None:
        hashed: str = get_password_hash("the-real-one")
        db_user: FakeRow = FakeRow(login="user_alice", password=hashed)
        authenticate_user_use_case._repo.get = AsyncCallRecorder(return_value=db_user)

        with pytest.raises(WrongPasswordException):
            await authenticate_user_use_case.execute(
                login="user_alice", password="not-it"
            )
