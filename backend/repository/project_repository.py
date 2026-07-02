from sqlalchemy import  text
from schemas.project_schemas import (StartProjectDateUpdate,
                                            ProjectTypeUpdate,
                                            KeyTable)
from uuid import UUID
from config import settings
    
    
SCHEMA = f'{settings.DB_SCHEMA}'


async def get_all_project_types_repository(session):
    project_types = await session.execute(
            text(f'''SELECT 
                    unique_project_type_key, project_type
                    FROM "{SCHEMA}".project_type_dict
                    WHERE is_deleted=False
                    ORDER BY project_type
                    ''')
            )
    return [dict(row._mapping) for row in project_types]

async def get_unpaid_projects_repository(session):
    unpaid_projects = await session.execute(
            text(f'''SELECT 
                    unique_project_key,
                    project_date,
                    company_name,
                    project_type,
                    comment,
                    project_budjet,
                    extra_work_price,
                    extra_work_hours,
                    total_extra_pay,
                    fact_payment,
                    "%_paid" as percent_paid
                FROM "{SCHEMA}".final_dashboard 
                WHERE "%_paid" < 1
                ORDER BY project_date DESC
                ''')
            )
    return [dict(row._mapping) for row in unpaid_projects]
    
async def get_project_repository(session, project_id: UUID):
    project = await session.execute(
            text(f'''SELECT
                    unique_project_key,
                    company_name,
                    project_type,
                    project_date,
                    comment,
                    fact_payment,
                    project_budjet,
                    extra_work_price,
                    extra_work_hours
                    FROM "{SCHEMA}".final_dashboard
                    WHERE unique_project_key = :project_id
                    '''),
                {
                    "project_id": project_id
                } 
            )
    return [dict(row._mapping) for row in project]
    
async def get_start_project_date_repository(session, project_id: UUID):
    project_date = await session.execute(
                    text(f"""
                        SELECT
                            unique_project_date_key,
                            unique_project_key,
                            project_date,
                            update_date,
                            is_deleted,
                            deleted_at
                        FROM "{SCHEMA}".start_project_date_table
                        WHERE unique_project_key = :project_id and is_deleted = False
                    """),
                    {
                        "project_id": project_id
                    }
                    )
    return [dict(row._mapping) for row in project_date]
  
async def insert_start_project_date_repository(session, payload: StartProjectDateUpdate):
    await session.execute(
            text(f"""
                INSERT INTO "{SCHEMA}".start_project_date_table
                (
                    unique_project_date_key,
                    unique_project_key,
                    project_date,
                    update_date,
                    is_deleted,
                    deleted_at
                )
                VALUES
                (
                    :new_id,
                    :project_id,
                    :project_date,
                    now(),
                    False,
                    null
                )
            """),
            {
                "new_id":  payload.unique_project_date_key,
                "project_id": payload.unique_project_key,
                "project_date": payload.project_date
            }
            )
    
async def delete_start_project_date_repository(session, project_id: UUID):
    await session.execute(
                text(f"""
                    UPDATE "{SCHEMA}".start_project_date_table
                    SET is_deleted = true,
                        deleted_at = now()
                    WHERE unique_project_key = :project_id and is_deleted = False
                """), 
                {
                    "project_id": project_id
                }
            )

async def get_project_type_repository(session, project_id: UUID):
    project_type = await session.execute(
                text(f"""
                    SELECT
                        A.project_type,
                        A.unique_project_type_key,
                        A.is_deleted,
                        A.deleted_at
                    FROM "{SCHEMA}".project_type_dict A
                    LEFT JOIN "{SCHEMA}".key_table AS B
                    ON A.unique_project_type_key=B.unique_project_type_key
                    WHERE B.unique_project_key = :project_id AND A.is_deleted=False AND B.is_deleted=False
                """),
                {
                    "project_id": project_id
                    
                }
                )
    return [dict(row._mapping) for row in project_type]
     
async def insert_project_type_repository(session, payload: ProjectTypeUpdate):
    await session.execute(
            text(f"""
                INSERT INTO "{SCHEMA}".project_type_dict
                (
                    unique_project_type_key,
                    project_type,
                    update_date,
                    is_deleted,
                    deleted_at
                )
                VALUES
                (
                    :new_id,
                    :project_type,
                    now(),
                    False,
                    null
                )
            """),
            {
                "new_id": payload.unique_project_type_key,
                "project_type": payload.project_type
                
            }
            )
    
async def delete_project_type_repository(session, project_id: UUID):
    await session.execute(
                text(f"""
                    UPDATE "{SCHEMA}".project_type_dict
                    SET is_deleted = true,
                        deleted_at = now()
                    WHERE unique_project_type_key = :project_id and is_deleted = False
                """), 
                {
                    "project_id": project_id
                }
            )

async def get_key_table_repository(session, project_id: UUID):
    key_table = await session.execute(
                text(f"""
                    SELECT
                        unique_project_key,
                        unique_company_key,
                        unique_project_type_key,
                        unique_comment_key,
                        unique_income_project_key,
                        unique_fix_payment_key,
                        unique_hourly_payment_key,
                        unique_project_date_key,
                        is_deleted,
                        deleted_at
                    FROM "{SCHEMA}".key_table
                    WHERE unique_project_key = :project_id AND is_deleted=False
                """),
                {
                    "project_id": project_id
                    
                }
                )
    row = key_table.mappings().first()

    if row is None:
        return None

    return KeyTable(**row)
   
async def insert_key_table_repository(session, keys):
    await session.execute(
            text(f"""
                INSERT INTO "{SCHEMA}".key_table
                (   
                    unique_project_key,
                    unique_company_key,
                    unique_project_type_key,
                    unique_comment_key,
                    unique_income_project_key,
                    unique_fix_payment_key,
                    unique_hourly_payment_key,
                    unique_project_date_key,
                    is_deleted,
                    deleted_at
                )
                VALUES
                (   
                    :unique_project_key,
                    :unique_company_key,
                    :unique_project_type_key,
                    :unique_comment_key,
                    :unique_income_project_key,
                    :unique_fix_payment_key,
                    :unique_hourly_payment_key,
                    :unique_project_date_key,
                    False,
                    null
                )
            """),
            {   
                "unique_project_key": keys.unique_project_key,
                "unique_company_key": keys.unique_company_key,
                "unique_project_type_key": keys.unique_project_type_key,
                "unique_comment_key": keys.unique_comment_key,
                "unique_income_project_key": keys.unique_income_project_key,
                "unique_fix_payment_key": keys.unique_fix_payment_key,
                "unique_hourly_payment_key": keys.unique_hourly_payment_key,
                "unique_project_date_key": keys.unique_project_date_key
            }
            )
    
async def delete_key_table_repository(session, project_id):
    await session.execute(
                text(f"""
                    UPDATE "{SCHEMA}".key_table
                    SET is_deleted = true,
                        deleted_at = now()
                    WHERE unique_project_key = :project_id and is_deleted = False
                """), 
                {
                    "project_id": project_id
                }
            )
    