from db import SessionLocal
from logger import logger
from uuid import UUID, uuid4
from schemas.comment_schemas import (CommentUpdate)
from repository.dashboard_repository import (refresh_dashboard_repository)
from repository.comment_repository import (get_comment_repository,
                                           insert_comment_repository,
                                           delete_comment_repository)
from repository.project_repository import (get_key_table_repository,
                                           delete_key_table_repository,
                                           insert_key_table_repository)

async def get_comment_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            project_types = await get_comment_repository(session, project_id)
            
            logger.info("comment loaded")
            
            return project_types
        
    except Exception:
        
        logger.exception("comment load failed")
        
        raise

    
async def delete_comment_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            await delete_comment_repository(session, project_id)
            
            await refresh_dashboard_repository(session)

            await session.commit()
            
            logger.info("comment soft delete loaded")
            
            return {"status": "ok"}
    except Exception:
        
        logger.exception("comment soft delete failed")
        
        raise
       
async def _update_comment(
    session,
    current_key: UUID,
    project_id: UUID,
    new_comment: str
) -> UUID:
    
    new_key = uuid4()
        
    payload = CommentUpdate (unique_comment_key=new_key,
                        unique_project_key=project_id,
                        comment=new_comment)

    data = await get_comment_repository(session, project_id)

    if not data:
        print("_update_comment_1")
        await insert_comment_repository(session, payload)

        return new_key

    old_comment = data[0]["comment"]

    if old_comment == new_comment:
        print("_update_comment_2")
        return current_key

    else:
        await delete_comment_repository(session, project_id)
        print("_update_comment_3")
        await insert_comment_repository(session, payload)

        return new_key

async def insert_comment_service(project_id: UUID, payload: CommentUpdate):

    try:
        async with SessionLocal() as session:
            
            keys = await get_key_table_repository(session, project_id)
        
            keys.unique_project_key = project_id
            
            current_key = keys.unique_comment_key

            keys.unique_comment_key = await _update_comment(session = session,
                                                            current_key = keys.unique_comment_key,
                                                            project_id = project_id,
                                                            new_comment = payload.comment
                                                        )
            
            if keys.unique_comment_key != current_key:

                await delete_key_table_repository(session,
                                            project_id)
            
                await insert_key_table_repository(session,
                                                keys)


                await refresh_dashboard_repository(session)

                await session.commit()

                logger.info("Comment updated")

            return {
                "status": "ok",
                "unique_comment_key": keys.unique_comment_key
            }

    except Exception:
        logger.exception("Comment update failed")
        raise
    
