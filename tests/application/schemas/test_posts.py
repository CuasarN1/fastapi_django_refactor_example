import pytest
from pydantic import ValidationError

from application.schemas.posts import (
    PostCreateSchema,
    PostResponseSchema,
    PostImageResponse,
)


class TestPostCreateSchema:
    def test_image_path_defaults_to_none(self) -> None:
        schema: PostCreateSchema = PostCreateSchema(title="t", text="x", user_id="user_1")
        assert schema.image_path is None

    def test_explicit_image_path_is_kept(self) -> None:
        schema: PostCreateSchema = PostCreateSchema(
            title="t", text="x", user_id="user_1", image_path="img"
        )
        assert schema.image_path == "img"

    def test_requires_title(self) -> None:
        with pytest.raises(ValidationError):
            PostCreateSchema(text="x", user_id="user_1")  # type: ignore[call-arg]

    def test_requires_text(self) -> None:
        with pytest.raises(ValidationError):
            PostCreateSchema(title="t", user_id="user_1")  # type: ignore[call-arg]

    def test_requires_user_id(self) -> None:
        with pytest.raises(ValidationError):
            PostCreateSchema(title="t", text="x")  # type: ignore[call-arg]


class TestPostResponseSchema:
    def test_built_from_attributes(self) -> None:
        class Obj:
            id: int = 1
            title: str = "t"
            text: str = "x"
            user_id: str = "user_1"
            image_path: str | None = None

        schema: PostResponseSchema = PostResponseSchema.model_validate(Obj())
        assert schema.id == 1
        assert schema.title == "t"
        assert schema.image_path is None


class TestPostImageResponse:
    def test_holds_image_path(self) -> None:
        resp: PostImageResponse = PostImageResponse(image_path="some-uuid")
        assert resp.image_path == "some-uuid"

    def test_requires_image_path(self) -> None:
        with pytest.raises(ValidationError):
            PostImageResponse()  # type: ignore[call-arg]
