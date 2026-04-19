from application.infrastructure.sqlite.database import database
from application.infrastructure.sqlite.repositories.posts import PostsRepository
from application.schemas.posts import PostCreateSchema, PostResponseSchema


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostsRepository()

    async def execute(self, create_post: PostCreateSchema) -> PostResponseSchema:
        with self._database.session() as session:
            post = self._repo.create(session=session, create_post=create_post)

        return PostResponseSchema.model_validate(obj=post)
