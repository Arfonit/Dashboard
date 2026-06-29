from db import SessionLocal
from logger import logger
from uuid import UUID, uuid4
from datetime import date
from schemas.project_schemas import (Project,
                                     StartProjectDateUpdate,
                                     ProjectTypeUpdate)
from repository.dashboard_repository import (refresh_dashboard_repository)
from repository.project_repository import (get_all_project_types_repository,
                                           get_unpaid_projects_repository,
                                           get_project_repository,
                                           get_start_project_date_repository,
                                           insert_start_project_date_repository,
                                           delete_start_project_date_repository,
                                           get_project_type_repository,
                                           insert_project_type_repository,
                                           delete_project_type_repository,
                                           get_key_table_repository,
                                           insert_key_table_repository,
                                           delete_key_table_repository)
from services.comment_service import (_update_comment)
from services.company_service import (_update_company_name)
#from services.dashboard_service import (_update_dashboard)
from services.income_service import (_update_HourlyPayment, _update_FixPayment)
from services.payment_service import (_update_fact_payment)


async def get_all_project_types_service():
    try:
        async with SessionLocal() as session:
            
            project_types = await get_all_project_types_repository(session)
            
            logger.info("all_project_types loaded")
            
            return project_types
        
    except Exception:
        
        logger.exception("all_project_types load failed")
        
        raise

async def get_unpaid_projects_service():
    try:
        async with SessionLocal() as session:
            
            unpaid_projects = await get_unpaid_projects_repository(session)
            
            logger.info("unpaid_projects loaded")
            
            return unpaid_projects
    except Exception:
        
        logger.exception("unpaid_projects load failed")
        
        raise
    
    
async def get_project_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            result = await get_project_repository(session,project_id)
            
            logger.info("project loaded")
            
            return result
    except Exception:
        
        logger.exception("project load failed")
        
        raise
    
async def get_start_project_date_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            start_project_date = await get_start_project_date_repository(session, project_id)
            
            logger.info("start_project_date loaded")
            
            return start_project_date
    except Exception:
        
        logger.exception("start_project_date load failed")
        
        raise    
    
    
async def delete_start_project_date_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            await delete_start_project_date_repository(session, project_id)
            
            await refresh_dashboard_repository(session)

            await session.commit()
            
            logger.info("start_project_date soft delete loaded")
            
            return {"status": "ok"}
    except Exception:
        
        logger.exception("start_project_date soft delete failed")
        
        raise

async def get_project_type_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            project_types = await get_project_type_repository(session, project_id)
            
            logger.info("project_type loaded")
            
            return project_types
        
    except Exception:
        
        logger.exception("project_type load failed")
        
        raise

    
async def delete_project_type_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            await delete_project_type_repository(session, project_id)
            
            await refresh_dashboard_repository(session)

            await session.commit()
            
            logger.info("project_type soft delete loaded")
            
            return {"status": "ok"}
    except Exception:
        
        logger.exception("project_type soft delete failed")
        
        raise
    
async def _update_project_type(
    session,
    current_key: UUID,
    project_id: UUID,
    new_project_type: str
) -> UUID:

    new_key = uuid4()
    
    payload = ProjectTypeUpdate (unique_project_type_key = new_key,
                                                unique_project_key = project_id,
                                                project_type = new_project_type)
    
    data = await get_all_project_types_repository(session)
    
    for row in data:
        if row["project_type"] == new_project_type:
            current_key_existed = row["unique_project_type_key"]
    
    print("_update_project_type_1", row["unique_project_type_key"])

    current_project_types = [row["project_type"] for row in data]
    print("old_project_type", current_project_types, "new_project_type",new_project_type, new_project_type in current_project_types)
    if new_project_type in current_project_types:
        current_key = current_key_existed
        print("_update_project_type_2", current_key)
        return current_key
    else:
        print("_update_project_type_3", new_key)
        await insert_project_type_repository(session, payload)

        return new_key  

async def insert_project_type_service(project_id: UUID, payload: ProjectTypeUpdate):

    try:
        async with SessionLocal() as session:
            
            keys = await get_key_table_repository(session, project_id)
        
            keys.unique_project_key = project_id
            
            current_key=keys.unique_project_type_key

            keys.unique_project_type_key = await _update_project_type(session=session,
                                                                    current_key=keys.unique_project_type_key,
                                                                    project_id=project_id,
                                                                    new_project_type=payload.project_type)

            if keys.unique_project_type_key != current_key:
                await delete_key_table_repository(session,
                                            project_id)
            
                await insert_key_table_repository(session,
                                                keys)


                await refresh_dashboard_repository(session)

                await session.commit()

                logger.info("project_type updated")

            return {
                "status": "ok",
                "start_project_date": keys.unique_project_type_key
            }

    except Exception:
        logger.exception("project_type update failed")
        raise

async def _update_project_date(
    session,
    current_key: UUID,
    project_id: UUID,
    new_project_date: date
) -> UUID:

    new_key = uuid4()
    
    payload = StartProjectDateUpdate (unique_project_date_key=new_key,
                                    unique_project_key=project_id,
                                    project_date=new_project_date)
    
    data = await get_start_project_date_repository(session, project_id)

    if not data:
        print("_update_project_date_1")
        await insert_start_project_date_repository(session, payload)
        
        return new_key  

    else:
        old_project_date = data[0]["project_date"]

        if old_project_date == new_project_date:
            print("_update_project_date_2")
            return current_key
        
        else:

            await delete_start_project_date_repository(session, project_id)
            print("_update_project_date_3")
            await insert_start_project_date_repository(session, payload)

            return new_key  

async def insert_start_project_date_service(project_id: UUID, payload: StartProjectDateUpdate):

    try:
        async with SessionLocal() as session:
            
            keys = await get_key_table_repository(session, project_id)
        
            keys.unique_project_key = project_id
            
            current_key=keys.unique_project_date_key

            keys.unique_project_date_key = await _update_project_date(session=session,
                                                                    current_key=keys.unique_project_date_key,
                                                                    project_id=project_id,
                                                                    new_project_date=payload.project_date)

            if keys.unique_project_date_key != current_key:
                await delete_key_table_repository(session,
                                            project_id)
            
                await insert_key_table_repository(session,
                                                keys)


                await refresh_dashboard_repository(session)

                await session.commit()

                logger.info("start_project_date updated")

            return {
                "status": "ok",
                "unique_project_date_key": keys.unique_project_date_key
            }

    except Exception:
        logger.exception("start_project_date update failed")
        raise

async def update_project_service(project_id: UUID, payload: Project, change_type: str):

    async with SessionLocal() as session:
        
        print("project_id_look", project_id)

        keys = await get_key_table_repository(session, project_id)
        
        if change_type == 'create':
            project_id = uuid4()

        print("keys_look", keys)
            
        keys.unique_project_key = project_id
        print("unique_company_key_start")
        keys.unique_company_key = await _update_company_name(session=session,
                                                            current_key=keys.unique_company_key,
                                                            project_id=project_id,
                                                            new_company_name=payload.company_name)
        print("unique_company_key_end")
        print("unique_project_type_key_start")
        keys.unique_project_type_key = await _update_project_type (session=session,
                                                        current_key=keys.unique_project_type_key,
                                                        project_id=project_id,
                                                        new_project_type=payload.project_type)
        print("unique_project_type_key_end")
        print("unique_comment_key_start")
        keys.unique_comment_key = await _update_comment(session=session,
                                                        current_key=keys.unique_comment_key,
                                                        project_id=project_id,
                                                        new_comment=payload.comment)
        print("unique_comment_key_end")
        print("unique_income_project_key_start")
        keys.unique_income_project_key = await _update_fact_payment(session=session,
                                                                    current_key=keys.unique_income_project_key,
                                                                    project_id=project_id,
                                                                    new_fact_payment=payload.fact_payment)
        print("unique_income_project_key_end")
        print("unique_fix_payment_key_start")
        keys.unique_fix_payment_key = await _update_FixPayment(session=session,
                                                                    current_key=keys.unique_fix_payment_key,
                                                                    project_id=project_id,
                                                                    new_fix_payment=payload.project_budjet)
        print("unique_fix_payment_key_end")
        print("unique_hourly_payment_key_start")
        keys.unique_hourly_payment_key = await _update_HourlyPayment(session=session,
                                                                    current_key=keys.unique_hourly_payment_key,
                                                                    project_id=project_id,
                                                                    new_extra_work_price=payload.extra_work_price,
                                                                    new_extra_work_hours=payload.extra_work_hours)
        print("unique_hourly_payment_key_end")
        print("unique_project_date_key_start")
        keys.unique_project_date_key = await _update_project_date(session=session,
                                                                    current_key=keys.unique_project_date_key,
                                                                    project_id=project_id,
                                                                    new_project_date=payload.project_date)
        print("unique_project_date_key_end")
        print("keys_look_end", keys)
        await delete_key_table_repository(session,
                                          project_id)
        
        await insert_key_table_repository(session,
                                        keys)


        await refresh_dashboard_repository(session)

        await session.commit()