from pathlib import Path

import pytest
from fastapi.responses import FileResponse

from application.domain.post.use_cases.get_post_image import GetPostImageUseCase
from application.core.exceptions.database_exceptions import EntityNotFoundException
from application.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    PostHasNoImageException,
)

from tests.mocks import AsyncCallRecorder, FakeRow


class TestGetPostImageUseCase:
    async def test_returns_file_response_when_image_exists(
        self, get_post_image_use_case: GetPostImageUseCase, tmp_path: Path
    ) -> None:
        image_name: str = "abc"
        (tmp_path / f"{image_name}.jpeg").write_bytes(b"fake")

        db_post: FakeRow = FakeRow(id=1, image_path=image_name)
        get_post_image_use_case._repo.get = AsyncCallRecorder(return_value=db_post)

        response: FileResponse = await get_post_image_use_case.execute(post_id=1)

        assert isinstance(response, FileResponse)
        assert response.media_type == "image/jpeg"

    async def test_raises_when_post_not_found(
        self, get_post_image_use_case: GetPostImageUseCase
    ) -> None:
        get_post_image_use_case._repo.get = AsyncCallRecorder(
            side_effect=EntityNotFoundException()
        )

        with pytest.raises(PostNotFoundByIdException):
            await get_post_image_use_case.execute(post_id=42)

    async def test_raises_when_post_has_no_image(
        self, get_post_image_use_case: GetPostImageUseCase
    ) -> None:
        db_post: FakeRow = FakeRow(id=1, image_path=None)
        get_post_image_use_case._repo.get = AsyncCallRecorder(return_value=db_post)

        with pytest.raises(PostHasNoImageException):
            await get_post_image_use_case.execute(post_id=1)
