from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from application.infrastructure.sqlite.models.posts import Posts as PostModel
from application.schemas.posts import PostCreateSchema
from application.core.exceptions.database_exceptions import EntityNotFoundException


class PostsRepository:
    def __init__(self):
        self._model: Type[PostModel] = PostModel

    def get(self, session: Session, id: int) -> PostModel:
        query = (
            select(self._model)
            .where(self._model.id == id)
        )

        user = session.scalar(query)
        if not user:
            raise EntityNotFoundException()

        return user

    def create(self, session: Session, create_post: PostCreateSchema) -> PostModel:
        query = (
            insert(self._model)
            .values(create_post.model_dump())
            .returning(self._model)
        )

        post = session.scalar(query)

        return post
