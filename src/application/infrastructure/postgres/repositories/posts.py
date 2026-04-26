from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.infrastructure.postgres.models.posts import Posts as PostModel
from application.schemas.posts import PostCreateSchema
from application.core.exceptions.database_exceptions import EntityNotFoundException


class PostsRepository:
    def __init__(self):
        self._model: Type[PostModel] = PostModel

    async def get(self, session: AsyncSession, id: int) -> PostModel:
        query = (
            select(self._model)
            .where(self._model.id == id)
        )

        user = await session.scalar(query)
        if not user:
            raise EntityNotFoundException()

        return user

    async def create(self, session: AsyncSession, create_post: PostCreateSchema) -> PostModel:
        query = (
            insert(self._model)
            .values(create_post.model_dump())
            .returning(self._model)
        )

        post = await session.scalar(query)

        return post
