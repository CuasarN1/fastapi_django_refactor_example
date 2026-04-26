from fastapi.responses import FileResponse

from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostsRepository
from application.core.exceptions.database_exceptions import EntityNotFoundException
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException, PostHasNoImageException


class GetPostImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostsRepository()
        self.image_folder = "./../images"

    async def execute(self, post_id: int) -> FileResponse:
        try:
            async with self._database.session() as session:
                post = await self._repo.get(session=session, id=post_id)
        except EntityNotFoundException:
            raise PostNotFoundByIdException(id=post_id)

        if not post.image_path:
            raise PostHasNoImageException()

        full_image_path: str = f"{self.image_folder}/{post.image_path}.jpeg"
        return FileResponse(full_image_path, media_type="image/jpeg")
