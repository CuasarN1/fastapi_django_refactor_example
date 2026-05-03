from typing import Any

from application.domain.post.use_cases.create_post import CreatePostUseCase
from application.schemas.posts import PostCreateSchema

from tests.mocks import AsyncCallRecorder, FakeRow


class TestCreatePostUseCase:
    async def test_creates_post_and_returns_response(
        self, create_post_use_case: CreatePostUseCase
    ) -> None:
        db_post: FakeRow = FakeRow(
            id=1, title="t", text="x", user_id="user_1", image_path=None
        )
        create_post_use_case._repo.create = AsyncCallRecorder(return_value=db_post)

        payload: PostCreateSchema = PostCreateSchema(title="t", text="x", user_id="user_1")
        result: Any = await create_post_use_case.execute(create_post=payload)

        assert result.id == 1
        assert result.title == "t"
        assert result.image_path is None
        create_post_use_case._repo.create.assert_awaited_once()
