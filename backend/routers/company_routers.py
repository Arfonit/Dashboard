from fastapi import APIRouter
from uuid import UUID
from backend.schemas.company_schemas import (CompanyNameUpdate)
from services.company_service import (get_company_name_service,
                                      insert_company_name_service,
                                      delete_company_name_service,
                                      get_all_company_names_service)

router = APIRouter()

@router.get("/get_company_name/{project_id}")
async def get_company_name(project_id: UUID):
    return await get_company_name_service(project_id)

@router.post("/post_company_name/{project_id}")
async def insert_company_name(project_id: UUID, payload: CompanyNameUpdate):
    return await insert_company_name_service(project_id, payload)

@router.delete("/delete_company_name/{project_id}")
async def delete_company_name(project_id: UUID):
    return await delete_company_name_service(project_id)

@router.get("/get_all_companies")
async def get_all_company_names():
    return await get_all_company_names_service()