from pydantic import BaseModel, Field, ConfigDict


class PostCreateSchema(BaseModel):
    title: str = Field(...)
    text: str = Field(...)
    user_id: str = Field(...)
    image_path: str | None = Field(None)


class PostResponseSchema(BaseModel):
    id: int = Field(...)
    title: str = Field(...)
    text: str = Field(...)
    user_id: str = Field(...)
    image_path: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class PostImageResponse(BaseModel):
    image_path: str
