from sqlalchemy import  text
from schemas.income_schemas import (IncomeCreate, 
                                            FixPaymentUpdate,
                                            HourlyPaymentUpdate
                                            )
from uuid import UUID
from config import settings
    
    
SCHEMA = f'{settings.DB_SCHEMA}'


async def get_income_by_year_repository(session):
    income_by_year = await session.execute(
            text(f'''SELECT 
                    EXTRACT(YEAR FROM income_date) as year,
                    SUM(COALESCE(amount, 0)) as total_income
                FROM "{SCHEMA}".income_by_date_table
                GROUP BY EXTRACT(YEAR FROM income_date)
                ORDER BY year DESC''')
    )
    return [dict(row._mapping) for row in income_by_year]

async def get_income_by_month_repository(session, year: int):
    income_by_month=await session.execute(
                    text(f'''SELECT 
                            EXTRACT(MONTH FROM income_date) as month,
                            SUM(COALESCE(amount, 0)) as total_income
                        FROM "{SCHEMA}".income_by_date_table
                        WHERE  EXTRACT(YEAR FROM income_date) = :year
                        GROUP BY EXTRACT(MONTH  FROM income_date)
                        ORDER BY month DESC'''),
                    {
                        "year": year
                    }
                )
    return [dict(row._mapping) for row in income_by_month]

async def post_income_repository(session, payload: IncomeCreate):
    await session.execute(
                text(f"""
                    INSERT INTO "{SCHEMA}".income_by_date_table 
                        (
                            unique_income_key,
                            income_date, 
                            amount, 
                            update_date, 
                            is_deleted, 
                            deleted_at
                        )
                    VALUES 
                        (
                            gen_random_uuid(),
                            :income_date,
                            :amount,
                            now(),
                            False,
                            null
                        )
                """),
                {
                    "income_date": payload.income_date, 
                    "amount": payload.amount
                }
            )
            
    
async def soft_delete_repository(session, payload: IncomeCreate):
    await session.execute(
        text(f"""
             UPDATE "{SCHEMA}".income_by_date_table
                    SET is_deleted = true,
                        deleted_at = now()
                    WHERE unique_income_key = :unique_income_key and is_deleted = False
                """), 
                {
                    "unique_income_key": payload.unique_income_key
                }
    )
    
    
async def get_fix_income_repository(session,project_id: UUID):
    fix_income = await session.execute(
        text(f"""
            SELECT
                unique_fix_payment_key,
                unique_project_key,
                update_date,
                project_budjet,
                is_deleted, 
                deleted_at
            FROM "{SCHEMA}".projects_with_fix_payment_table
            WHERE unique_project_key = :project_id AND is_deleted=False
        """),
        {
            "project_id": project_id
        }
        )
    return [dict(row._mapping) for row in fix_income]
          
async def insert_fix_income_repository(session, payload: FixPaymentUpdate):
    await session.execute(
        text(f"""
            INSERT INTO "{SCHEMA}".projects_with_fix_payment_table
            (   
                unique_fix_payment_key,
                unique_project_key,
                update_date,
                project_budjet,
                is_deleted, 
                deleted_at
            )
            VALUES
            (   
                :new_id,
                :project_id,
                now(),
                :project_budjet,
                False,
                null
            )
        """),
        {
            "new_id": payload.unique_fix_payment_key,
            "project_id": payload.unique_project_key,
            "project_budjet": payload.project_budjet
        }
        )
     
async def delete_fix_income_repository(session, project_id: UUID):
    await session.execute(
                text(f"""
                    UPDATE "{SCHEMA}".projects_with_fix_payment_table
                    SET is_deleted = true,
                        deleted_at = now()
                    WHERE unique_project_key = :project_id and is_deleted = False
                """), 
                {
                    "project_id": project_id
                }
            )

async def get_hourly_income_repository(session, project_id: UUID):
    hourly_income = await session.execute(
                    text(f"""
                        SELECT
                            unique_hourly_payment_key,
                            unique_project_key,
                            update_date,
                            extra_work_price,
                            extra_work_hours,
                            is_deleted, 
                            deleted_at
                    FROM "{SCHEMA}".projects_with_hourly_payment_table
                    WHERE unique_project_key = :project_id and is_deleted = False
                    """),
                    {
                        "project_id": project_id
                    }
                    )
    return [dict(row._mapping) for row in hourly_income]
    
async def insert_hourly_income_repository(session, payload: HourlyPaymentUpdate):
    await session.execute(
    text(f"""
        INSERT INTO "{SCHEMA}".projects_with_hourly_payment_table
        (
            unique_hourly_payment_key,
            unique_project_key,
            extra_work_price,
            extra_work_hours,
            update_date,
            is_deleted, 
            deleted_at
        )
        VALUES
        (
            :new_id,
            :project_id,
            :extra_work_price,
            :extra_work_hours,
            now(),
            False,
            null
        )
    """),
    {
        "new_id": payload.unique_hourly_payment_key,
        "project_id": payload.unique_project_key,
        "extra_work_price": payload.extra_work_price,
        "extra_work_hours": payload.extra_work_hours
    }
    )
    
async def delete_hourly_income_repository(session, project_id: UUID):
    await session.execute(
                text(f"""
                    UPDATE "{SCHEMA}".projects_with_hourly_payment_table
                    SET is_deleted = true,
                        deleted_at = now()
                    WHERE unique_project_key = :project_id and is_deleted = False
                """), 
                {
                    "project_id": project_id
                }
            )

    