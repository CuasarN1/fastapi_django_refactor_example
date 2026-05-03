from typing import Any

import pytest

from application.domain.user.use_cases.get_user_by_login import (
    GetUserByLoginUseCase,
)
from application.core.exceptions.database_exceptions import EntityNotFoundException
from application.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from application.schemas.users import User

from tests.mocks import AsyncCallRecorder, FakeRow


class TestGetUserByLoginUseCase:
    async def test_returns_user_when_found(
        self,
        get_user_by_login_use_case: GetUserByLoginUseCase,
        current_user: User,
    ) -> None:
        db_user: FakeRow = FakeRow(login="user_target", password="hashed")
        get_user_by_login_use_case._repo.get = AsyncCallRecorder(return_value=db_user)

        result: Any = await get_user_by_login_use_case.execute(
            login="user_target", current_user=current_user
        )

        assert result.login == "user_target"

    async def test_raises_when_user_not_found(
        self,
        get_user_by_login_use_case: GetUserByLoginUseCase,
        current_user: User,
    ) -> None:
        get_user_by_login_use_case._repo.get = AsyncCallRecorder(
            side_effect=EntityNotFoundException()
        )

        with pytest.raises(UserNotFoundByLoginException) as exc_info:
            await get_user_by_login_use_case.execute(
                login="ghost", current_user=current_user
            )

        assert "ghost" in exc_info.value.get_detail()
