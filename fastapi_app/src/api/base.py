from fastapi import APIRouter, status, HTTPException, Depends

from schemas.posts import PostRequestSchema, PostResponseSchema
from services.auth import AuthService

router = APIRouter()


@router.post(
    "/test_json",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponseSchema,
    dependencies=[Depends(AuthService.get_current_user)]
)
async def test_json(post: PostRequestSchema) -> dict:
    if len(post.text) < 3:
        raise HTTPException(
            detail="Длина поста должна быть не меньше 3 символов",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    response = {
        "post_text": post.text,
        "author_name": post.author.login
    }

    return PostResponseSchema.model_validate(obj=response)
