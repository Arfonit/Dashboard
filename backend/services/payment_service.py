from db import SessionLocal
from logger import logger
from uuid import UUID, uuid4
from backend.schemas.payment_schemas import (FactPaymentUpdate)
from repository.dashboard_repository import (refresh_dashboard_repository)
from repository.payment_repository import (get_fact_payment_repository,
                                           insert_fact_payment_repository,
                                           delete_fact_payment_repository,
                                           get_total_fact_payment_repository)
from repository.project_repository import (get_key_table_repository,
                                           insert_key_table_repository,
                                           delete_key_table_repository)


async def get_total_fact_payment_service():
    try:
        async with SessionLocal() as session:
            
            fact_payment_total = await get_total_fact_payment_repository(session)
            
            logger.info("fact_payment_total loaded")
            
            return fact_payment_total
    except Exception:
        
        logger.exception("fact_payment_total load failed")
        
        raise    
    
async def get_fact_payment_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            fact_payment = await get_fact_payment_repository(session, project_id)
            
            logger.info("fact_payment loaded")
            
            return fact_payment
    except Exception:
        
        logger.exception("fact_payment load failed")
        
        raise    
        
async def delete_fact_payment_service(project_id: UUID):
    try:
        async with SessionLocal() as session:
            
            await delete_fact_payment_repository(session, project_id)
            
            await refresh_dashboard_repository(session)

            await session.commit()
            
            logger.info("fact_payment soft delete loaded")
            
            return {"status": "ok"}
    except Exception:
        
        logger.exception("fact_payment soft delete failed")
        
        raise
    
async def _update_fact_payment(
    session,
    current_key: UUID,
    project_id: UUID,
    new_fact_payment: float
) -> UUID:

    new_key = uuid4()

    payload = FactPaymentUpdate(unique_income_project_key = new_key,
                                    unique_project_key = project_id,
                                    fact_payment = new_fact_payment)
    
    data = await get_fact_payment_repository(session, project_id)

    if not data:
        print("_update_fact_payment_1")
        await insert_fact_payment_repository(session, payload)
        
        return new_key
        
    else:

        old_fact_payment = data[0]["fact_payment"]

        if old_fact_payment == new_fact_payment:
            print("_update_fact_payment_2")
            return current_key

        else:
            await delete_fact_payment_repository(session, project_id)
            print("_update_fact_payment_3")
            await insert_fact_payment_repository(session, payload)

            return new_key

async def insert_fact_payment_service(project_id: UUID, payload: FactPaymentUpdate):

    try:
        async with SessionLocal() as session:
            
            keys= await get_key_table_repository(session, project_id)
            
            keys.unique_project_key = project_id
            
            current_key= keys.unique_income_project_key

            keys.unique_income_project_key = await _update_fact_payment(session = session,
                                                                        current_key= keys.unique_income_project_key,
                                                                        project_id = project_id,
                                                                        new_fact_payment = payload.fact_payment
                                                                    )
            
            if  keys.unique_income_project_key != current_key:
                await delete_key_table_repository(session,
                                            project_id)
            
                await insert_key_table_repository(session,
                                                keys)

                await refresh_dashboard_repository(session)

                await session.commit()

                logger.info("fact_payment updated")

            return {
                "status": "ok",
                "unique_income_project_key":  keys.unique_income_project_key
            }

    except Exception:
        logger.exception("fact_payment update failed")
        raise