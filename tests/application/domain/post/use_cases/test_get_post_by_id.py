from typing import Any

import pytest

from application.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from application.core.exceptions.database_exceptions import EntityNotFoundException
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException

from tests.mocks import AsyncCallRecorder, FakeRow


class TestGetPostByIdUseCase:
    async def test_returns_post_when_found(
        self, get_post_by_id_use_case: GetPostByIdUseCase
    ) -> None:
        db_post: FakeRow = FakeRow(
            id=7, title="t", text="x", user_id="user_1", image_path="img"
        )
        get_post_by_id_use_case._repo.get = AsyncCallRecorder(return_value=db_post)

        result: Any = await get_post_by_id_use_case.execute(post_id=7)

        assert result.id == 7
        assert result.image_path == "img"

    async def test_raises_when_post_missing(
        self, get_post_by_id_use_case: GetPostByIdUseCase
    ) -> None:
        get_post_by_id_use_case._repo.get = AsyncCallRecorder(
            side_effect=EntityNotFoundException()
        )

        with pytest.raises(PostNotFoundByIdException) as exc_info:
            await get_post_by_id_use_case.execute(post_id=999)

        assert "999" in exc_info.value.get_detail()
