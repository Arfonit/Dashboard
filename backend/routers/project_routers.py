from fastapi import APIRouter
from uuid import UUID
from backend.schemas.project_schemas import (Project,
                                             StartProjectDateUpdate,
                                             ProjectTypeUpdate)
from services.project_service import (get_all_project_types_service,
                                      get_unpaid_projects_service,
                                      get_project_service,
                                      get_start_project_date_service,
                                      insert_start_project_date_service,
                                      delete_start_project_date_service,
                                      get_project_type_service,
                                      insert_project_type_service,
                                      delete_project_type_service,
                                      update_project_service)


router = APIRouter()

@router.get("/get_all_project_types")
async def get_all_project_types():
    return await get_all_project_types_service()

@router.get("/get_unpaid_projects")
async def get_unpaid_projects():
    return await get_unpaid_projects_service()

@router.get("/project/{project_id}")
async def get_project(project_id: UUID):
    return await get_project_service(project_id)

@router.get("/get_start_project_date/{project_id}")
async def get_start_project_date(project_id: UUID):
    return await get_start_project_date_service(project_id)

@router.post("/post_start_project_date/{project_id}")
async def insert_start_project_date(project_id: UUID, payload: StartProjectDateUpdate):
    return await insert_start_project_date_service(project_id, payload)

@router.delete("/delete_start_project_date/{project_id}")
async def delete_start_project_date(project_id: UUID):
    return await delete_start_project_date_service(project_id)

@router.get("/get_project_types/{project_id}")
async def get_project_types(project_id: UUID):
    return await get_project_type_service(project_id)

@router.post("/post_project_type/{project_id}")
async def insert_project_type_date(project_id: UUID, payload: ProjectTypeUpdate):
    return await insert_project_type_service(project_id, payload)

@router.delete("/delete_project_type/{project_id}")
async def delete_project_type(project_id: UUID):
    return await delete_project_type_service(project_id)

@router.post("/post_project_update/{project_id}")
async def insert_key_table(project_id: UUID, change_type: str , payload: Project):
    return await update_project_service(project_id, payload, change_type)



