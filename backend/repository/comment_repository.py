from sqlalchemy import  text
from schemas.comment_schemas import (CommentUpdate)
from uuid import UUID
from config import settings
    
    
SCHEMA = f'{settings.DB_SCHEMA}'


async def get_comment_repository(session,project_id: UUID):
    comment = await session.execute(
            text(f"""
                SELECT 
                    unique_comment_key,
                    unique_project_key,
                    comment,
                    update_date,
                    is_deleted, 
                    deleted_at
                FROM "{SCHEMA}".comment_table
                WHERE unique_project_key = :project_id AND is_deleted=False
            """),
            {   
                "project_id": project_id
            }
            )
    return [dict(row._mapping) for row in comment]
    
    
async def insert_comment_repository(session, payload: CommentUpdate):
    await session.execute(
            text(f"""
                INSERT INTO "{SCHEMA}".comment_table
                (   
                    unique_comment_key,
                    unique_project_key,
                    comment,
                    update_date,
                    is_deleted, 
                    deleted_at
                )
                VALUES
                (   
                    :new_id,
                    :project_id,
                    :comment,
                    now(),
                    False,
                    null
                )
            """),
            {   
                "new_id": payload.unique_comment_key,
                "project_id": payload.unique_project_key,
                "comment": payload.comment
            }
            )
    
async def delete_comment_repository(session, project_id):
    await session.execute(
            text(f"""
                UPDATE "{SCHEMA}".comment_table
                SET is_deleted = true,
                    deleted_at = now()
                WHERE unique_project_key = :project_id and is_deleted = False
            """), 
            {
                "project_id": project_id
            }
            )