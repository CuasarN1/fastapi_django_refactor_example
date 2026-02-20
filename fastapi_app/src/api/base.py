from fastapi import APIRouter, status, HTTPException

from schemas.posts import Post


router = APIRouter()


@router.get("/hello_world", status_code=status.HTTP_200_OK)
async def get_hello_world() -> dict:
    response = {"text": "Hello, World!"}

    return response


@router.post("/test_json", status_code=status.HTTP_201_CREATED)
async def test_json(post: Post) -> dict:
    response = {
        "post_text": post.text,
        "author_name": post.author.login
    }

    return response
