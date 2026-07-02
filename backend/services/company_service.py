from db import SessionLocal
from logger import logger
from uuid import UUID, uuid4
from schemas.company_schemas import (CompanyNameUpdate)
from repository.dashboard_repository import (refresh_dashboard_repository)
from repository.company_repository import (get_company_name_repository,
                                           insert_company_name_repository,
                                           delete_company_name_repository,
                                           get_all_company_names_repository)
from repository.project_repository import (get_key_table_repository,
                                           delete_key_table_repository,
                                           insert_key_table_repository)


async def get_all_company_names_service():
    try:
        async with SessionLocal() as session:
            
            all_company_names = await get_all_company_names_repository(session)
            
            logger.info("all_company_names loaded")
            
            return all_company_names
    except Exception:
        
        logger.exception("all_company_names load failed")
        
        raise    

async def get_company_name_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            company_name = await get_company_name_repository(session, project_id)
            
            logger.info("company_name loaded")
            
            return company_name
    except Exception:
        
        logger.exception("company_name load failed")
        
        raise    

    
async def delete_company_name_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            await delete_company_name_repository(session, project_id)
            
            await refresh_dashboard_repository(session)

            await session.commit()
            
            logger.info("fact_payment soft delete loaded")
            
            return {"status": "ok"}
    except Exception:
        
        logger.exception("fact_payment soft delete failed")
        
        raise
    
async def _update_company_name(
    session,
    current_key: UUID,
    project_id: UUID,
    new_company_name: str
) -> UUID:
    
    new_key = uuid4()

    payload = CompanyNameUpdate (unique_company_key = new_key,
                                unique_project_key = project_id,
                                company_name = new_company_name)

    data = await get_all_company_names_repository(session)
    
    for row in data:
        if row["company_name"] == new_company_name:
            current_key_existed = row["unique_company_key"]

    company_name_dict = [row["company_name"] for row in data]

    if new_company_name in company_name_dict:
        current_key = current_key_existed
        print("_update_company_name_2",current_key)
        return current_key

    else:
        print("_update_company_name_3")
        await insert_company_name_repository(session, payload)

        return new_key

async def insert_company_name_service(project_id: UUID, payload: CompanyNameUpdate):
    try:
        async with SessionLocal() as session:
            
            keys = await get_key_table_repository(session, project_id)
        
            keys.unique_project_key = project_id
            
            current_key=keys.unique_company_key

            keys.unique_company_key = await _update_company_name(session=session,
                                                                    current_key=keys.unique_company_key,
                                                                    project_id=project_id,
                                                                    new_company_name=payload.company_name)
            
            if keys.unique_company_key != current_key:

                await delete_key_table_repository(session,
                                            project_id)
            
                await insert_key_table_repository(session,
                                                keys)


                await refresh_dashboard_repository(session)

                await session.commit()

                logger.info("company_name updated")

            return {
                "status": "ok",
                "unique_company_key": keys.unique_company_key
            }

    except Exception:
        logger.exception("company_name update failed")
        raise
    