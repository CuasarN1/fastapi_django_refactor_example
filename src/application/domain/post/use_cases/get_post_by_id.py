from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostsRepository
from application.schemas.posts import PostCreateSchema, PostResponseSchema
from application.core.exceptions.database_exceptions import EntityNotFoundException
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostsRepository()

    async def execute(self, post_id: int) -> PostResponseSchema:
        try:
            async with self._database.session() as session:
                post = await self._repo.get(session=session, id=post_id)
        except EntityNotFoundException:
            raise PostNotFoundByIdException(id=post_id)

        return PostResponseSchema.model_validate(obj=post)
