from pathlib import Path

import pytest

from application.domain.post.use_cases.add_post_image import AddPostImageUseCase
from application.core.exceptions.domain_exceptions import UploadFileIsNotImageException
from application.schemas.posts import PostImageResponse

from tests.mocks import FakeUploadFile


class TestAddPostImageUseCase:
    async def test_rejects_non_jpeg(
        self, add_post_image_use_case: AddPostImageUseCase
    ) -> None:
        with pytest.raises(UploadFileIsNotImageException):
            await add_post_image_use_case.execute(image=FakeUploadFile("photo.png"))

    async def test_saves_jpeg_and_returns_uuid(
        self, add_post_image_use_case: AddPostImageUseCase, tmp_path: Path
    ) -> None:
        result: PostImageResponse = await add_post_image_use_case.execute(
            image=FakeUploadFile("nice.jpeg", b"img-bytes")
        )

        assert result.image_path
        expected: Path = tmp_path / f"{result.image_path}.jpeg"
        assert expected.exists()
        assert expected.read_bytes() == b"img-bytes"

    async def test_each_upload_gets_unique_name(
        self, add_post_image_use_case: AddPostImageUseCase
    ) -> None:
        first: PostImageResponse = await add_post_image_use_case.execute(
            image=FakeUploadFile("a.jpeg", b"a")
        )
        second: PostImageResponse = await add_post_image_use_case.execute(
            image=FakeUploadFile("b.jpeg", b"b")
        )

        assert first.image_path != second.image_path
