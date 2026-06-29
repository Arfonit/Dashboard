from fastapi import APIRouter
from uuid import UUID
from backend.schemas.comment_schemas import (CommentUpdate)
from services.comment_service import (insert_comment_service,
                                      get_comment_service,
                                      delete_comment_service)

router = APIRouter()

@router.post("/post_comment/{project_id}")
async def insert_comment(project_id: UUID, payload: CommentUpdate):
    return await insert_comment_service(project_id, payload)

@router.delete("/delete_comment/{project_id}")
async def delete_comment(project_id: UUID):
    return await delete_comment_service(project_id)

@router.get("/get_comment/{project_id}")
async def get_comment(project_id: UUID):
    return await get_comment_service(project_id)
