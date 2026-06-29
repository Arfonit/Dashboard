from db import SessionLocal
from logger import logger
from schemas.income_schemas import (IncomeCreate,
                                    HourlyPaymentUpdate,
                                    FixPaymentUpdate)
from repository.dashboard_repository import (refresh_dashboard_repository)

from repository.income_repository import (get_income_by_year_repository,
                                          get_income_by_month_repository,
                                          post_income_repository,
                                          soft_delete_repository,
                                          get_fix_income_repository,
                                          insert_fix_income_repository,
                                          delete_fix_income_repository,
                                          get_hourly_income_repository,
                                          insert_hourly_income_repository,
                                          delete_hourly_income_repository)

from repository.project_repository import (get_key_table_repository,
                                           insert_key_table_repository,
                                           delete_key_table_repository)
from uuid import UUID, uuid4


async def get_income_by_year_service():
    try:
        async with SessionLocal() as session:
            
            income_by_year = await get_income_by_year_repository(session)

            logger.info("income_by_year loaded")

            return income_by_year  
          
    except Exception:
        
        logger.exception("income_by_year load failed")
        
        raise
    
async def get_income_by_month_service(year: int):
    try:
        async with SessionLocal() as session:
            
            income_by_month = await get_income_by_month_repository(session, year)

            logger.info("income_by_month loaded")

            return income_by_month  
          
    except Exception:
        
        logger.exception("income_by_month load failed")
        
        raise
    
async def post_income_service(payload: IncomeCreate):
    try:
        async with SessionLocal() as session:
            
            await post_income_repository(session, payload)
            
            await refresh_dashboard_repository(session)

            await session.commit()
            
            logger.info("income inserted")
            
            return {"status": "ok"}
    except Exception:
        
        logger.exception("income insert failed")
        
        raise
    
async def soft_delete_service():
    try:    
        async with SessionLocal() as session:
            
            await soft_delete_repository(session)
            
            await refresh_dashboard_repository(session)

            await session.commit()
            
            logger.info("delete_project_type soft deleted")
            
            return {"status": "ok"}
    except Exception:
        
        logger.exception("delete_project_type failed")
        
        raise    
    
async def get_fix_income_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            fix_income = await get_fix_income_repository(session, project_id)
            
            logger.info("fix_income loaded")
            
            return fix_income
    except Exception:
        
        logger.exception("fix_income load failed")
        
        raise    
        
async def delete_fix_income_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            await delete_fix_income_repository(session, project_id)
            
            await refresh_dashboard_repository(session)

            await session.commit()
            
            logger.info("payment_fixed soft delete loaded")
            
            return {"status": "ok"}
    except Exception:
        
        logger.exception("payment_fixed soft delete failed")
        
        raise

async def get_hourly_income_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            hourly_income = await get_hourly_income_repository(session, project_id)
            
            logger.info("hourly_income loaded")
            
            return hourly_income
    except Exception:
        
        logger.exception("hourly_income load failed")
        
        raise    
    
async def delete_hourly_income_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            await delete_hourly_income_repository(session, project_id)
            
            await refresh_dashboard_repository(session)

            await session.commit()
            
            logger.info("payment_hourly soft delete loaded")
            
            return {"status": "ok"}
    except Exception:
        
        logger.exception("payment_hourly soft delete failed")
        
        raise
    
async def _update_HourlyPayment(
    session,
    current_key: UUID,
    project_id: UUID,
    new_extra_work_price: float,
    new_extra_work_hours: float
) -> UUID:
    
    new_key = uuid4()
    
    payload = HourlyPaymentUpdate (unique_hourly_payment_key = new_key,
                            unique_project_key = project_id,
                            extra_work_price = new_extra_work_price,
                            extra_work_hours = new_extra_work_hours)

    data = await get_hourly_income_repository(session, project_id)

    if not data:
        print("_update_HourlyPayment_1")
        await insert_hourly_income_repository(session, payload)
        
        return new_key

    else:
        old_extra_work_price = data[0]["extra_work_price"]
        old_extra_work_hours = data[0]["extra_work_hours"]

        if old_extra_work_price == new_extra_work_price and old_extra_work_hours == new_extra_work_hours:
            print("_update_HourlyPayment_2")
            return current_key

        await delete_hourly_income_repository(session, project_id)
        print("_update_HourlyPayment_3")
        await insert_hourly_income_repository(session, payload)

        return new_key

async def insert_hourly_income_service(project_id: UUID, payload: HourlyPaymentUpdate):

    try:
        async with SessionLocal() as session:

            keys= await get_key_table_repository(session, project_id)
            
            keys.unique_project_key = project_id

            current_key = keys.unique_hourly_payment_key
            
            keys.unique_hourly_payment_key = await _update_HourlyPayment(session = session,
                                                                        current_key = keys.unique_hourly_payment_key,
                                                                        project_id = project_id,
                                                                        new_extra_work_price = payload.extra_work_price,
                                                                        new_extra_work_hours = payload.extra_work_hours
                                                                    )

            if keys.unique_hourly_payment_key!= current_key:
                await delete_key_table_repository(session,
                                            project_id)
            
                await insert_key_table_repository(session,
                                                keys)

                await refresh_dashboard_repository(session)

                await session.commit()

                logger.info("extra_work_price updated")

            return {
                "status": "ok",
                "unique_project_key": keys.unique_project_key,
                "unique_hourly_payment_key": keys.unique_hourly_payment_key 
            }

    except Exception:
        logger.exception("extra_work_price update failed")
        raise
    
async def _update_FixPayment(
    session,
    current_key: UUID,
    project_id: UUID,
    new_fix_payment: float
) -> UUID:
    
    new_key = uuid4()

    payload = FixPaymentUpdate (unique_fix_payment_key = new_key,
                                unique_project_key = project_id,
                                project_budjet = new_fix_payment)

    data = await get_fix_income_repository(session, project_id)

    if not data:
        
        await insert_fix_income_repository(session, payload)
        print("_update_FixPayment_1")
        return new_key

    else:
        old_fix_payment = data[0]["project_budjet"]

        if old_fix_payment == new_fix_payment:
            print("_update_FixPayment_2")
            return current_key
        
        else:

            await delete_fix_income_repository(session, project_id)
            print("_update_FixPayment_3")
            await insert_fix_income_repository(session, payload)

            return new_key

async def insert_fix_income_service(project_id: UUID, payload: FixPaymentUpdate):

    try:
        async with SessionLocal() as session:
            
            keys= await get_key_table_repository(session, project_id)
            
            keys.unique_project_key = project_id
            
            current_key = keys.unique_fix_payment_key

            keys.unique_fix_payment_key = await _update_FixPayment(session = session,
                                                                    current_key = keys.unique_fix_payment_key,
                                                                    project_id = project_id,
                                                                    new_fix_payment = payload.project_budjet
                                                                )
            if keys.unique_fix_payment_key != current_key:
            
                await delete_key_table_repository(session,
                                            project_id)
            
                await insert_key_table_repository(session,
                                                keys)

                await refresh_dashboard_repository(session)

                await session.commit()

                logger.info("fix_income updated")

            return {
                "status": "ok",
                "unique_fix_payment_key": keys.unique_fix_payment_key
            }

    except Exception:
        logger.exception("fix_income update failed")
        raise