from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse

from application.schemas.posts import PostCreateSchema, PostResponseSchema, PostImageResponse
from application.domain.post.use_cases.get_post_image import GetPostImageUseCase
from application.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from application.domain.post.use_cases.create_post import CreatePostUseCase
from application.domain.post.use_cases.add_post_image import AddPostImageUseCase
from application.api.depends import (
    get_post_by_id_use_case,
    create_post_use_case,
    get_post_image_use_case,
    add_post_image_use_case,
)
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException, PostHasNoImageException
from application.services.auth import AuthService

router = APIRouter(dependencies=[Depends(AuthService.get_current_user)])


@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
async def create_post(
    post: PostCreateSchema,
    use_case: CreatePostUseCase = Depends(create_post_use_case),
) -> PostResponseSchema:
    return await use_case.execute(create_post=post)


@router.get("/post/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def get_post_by_id(
    post_id: int,
    use_case: GetPostByIdUseCase = Depends(get_post_by_id_use_case),
) -> PostResponseSchema:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.get("/image/post/{post_id}", status_code=status.HTTP_200_OK, response_class=FileResponse)
async def get_post_image(
    post_id: int,
    use_case: GetPostImageUseCase = Depends(get_post_image_use_case),
) -> FileResponse:
    try:
        return await use_case.execute(post_id=post_id)
    except (PostNotFoundByIdException, PostHasNoImageException) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.post("/image/post", status_code=status.HTTP_201_CREATED, response_model=PostImageResponse)
async def add_post_image(
    image: UploadFile = File(...),
    use_case: AddPostImageUseCase = Depends(add_post_image_use_case),
) -> PostImageResponse:
    return await use_case.execute(image=image)
