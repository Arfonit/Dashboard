from sqlalchemy import  text
from backend.schemas.payment_schemas import (FactPaymentUpdate)
from uuid import UUID
from config import settings
    
    
SCHEMA = f'{settings.DB_SCHEMA}'


async def get_total_fact_payment_repository(session):
    fact_payment_total = await session.execute(
                text(f"""
                    SELECT
                        sum(fact_payment) as fact_payment_total
                    FROM "{SCHEMA}".income_by_project_table
                    WHERE unique_project_key = :project_id and is_deleted = False
                """)
                )
    return fact_payment_total

async def get_fact_payment_repository(session, project_id: UUID):
    fact_payment = await session.execute(
                text(f"""
                    SELECT
                        unique_income_project_key,
                        unique_project_key,
                        fact_payment,
                        update_date,
                        is_deleted, 
                        deleted_at
                    FROM "{SCHEMA}".income_by_project_table
                    WHERE unique_project_key = :project_id and is_deleted = False
                """),
                {
                    "project_id": project_id
                }
                )
    return [dict(row._mapping) for row in fact_payment]

 
async def insert_fact_payment_repository(session, payload: FactPaymentUpdate):
    await session.execute(
            text(f"""
                INSERT INTO "{SCHEMA}".income_by_project_table
                (
                    unique_income_project_key,
                    unique_project_key,
                    fact_payment,
                    update_date,
                    is_deleted, 
                    deleted_at
                )
                VALUES
                (
                    :new_id,
                    :project_id,
                    :fact_payment,
                    now(),
                    False,
                    null
                )
            """),
            {
                "new_id": payload.unique_income_project_key,
                "project_id": payload.unique_project_key,
                "fact_payment": payload.fact_payment
            }
            )

async def delete_fact_payment_repository(session, project_id: UUID):
    await session.execute(
                text(f"""
                    UPDATE "{SCHEMA}".income_by_project_table
                    SET is_deleted = true,
                        deleted_at = now()
                    WHERE unique_project_key = :project_id and is_deleted = False
                """), 
                {
                    "project_id": project_id
                }
            )