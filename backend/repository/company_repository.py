from sqlalchemy import  text
from schemas.company_schemas import (CompanyNameUpdate)
from uuid import UUID
from config import settings
    
    
SCHEMA = f'{settings.DB_SCHEMA}'

async def get_all_company_names_repository(session):
    all_company_names = await session.execute(
            text(f"""
                SELECT 
                    unique_company_key,
                    unique_group_key,
                    company_name,
                    company_group,
                    data_upload,
                    is_deleted,
                    deleted_at
                FROM "{SCHEMA}".company_name_dict
            """)
            )
    return [dict(row._mapping) for row in all_company_names]

async def get_company_name_repository(session, project_id: UUID):
    company_name = await session.execute(
            text(f"""
                SELECT 
                    A.unique_company_key,
                    A.unique_group_key,
                    A.company_name,
                    A.company_group,
                    A.data_upload,
                    A.is_deleted,
                    A.deleted_at
                FROM "{SCHEMA}".company_name_dict AS A
                LEFT JOIN "{SCHEMA}".key_table AS B
                ON A.unique_company_key=B.unique_company_key
                WHERE B.unique_project_key = :project_id AND A.is_deleted=False AND B.is_deleted=False
            """),
            {
                "project_id": project_id
            }
            )
    return [dict(row._mapping) for row in company_name]
    
async def insert_company_name_repository(session, payload: CompanyNameUpdate):
    await session.execute(
            text(f"""
                INSERT INTO "{SCHEMA}".company_name_dict
                (
                    unique_company_key,
                    unique_group_key,
                    company_name,
                    company_group,
                    data_upload,
                    is_deleted,
                    deleted_at
                )
                VALUES
                (
                    :new_id,
                    null,
                    :company_name,
                    null,
                    now(),
                    False,
                    null
                )
            """),
            {
                "new_id": payload.unique_company_key,
                "company_name": payload.company_name
            }
            )
    
async def delete_company_name_repository(session, project_id: UUID):
    await session.execute(
                text(f"""
                    UPDATE "{SCHEMA}".company_name_dict
                    SET is_deleted = true,
                        deleted_at = now()
                    WHERE unique_company_key = :project_id and is_deleted = False
                """), 
                {
                    "project_id": project_id
                }
            )
