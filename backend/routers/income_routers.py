from fastapi import APIRouter
from schemas.income_schemas import (IncomeCreate,
                                    FixPaymentUpdate,
                                    HourlyPaymentUpdate)
from services.income_service import (get_income_by_year_service,
                                     get_income_by_month_service,
                                     post_income_service,
                                     soft_delete_service,
                                     get_fix_income_service,
                                     insert_fix_income_service,
                                     delete_fix_income_service,
                                     get_hourly_income_service,
                                     insert_hourly_income_service,
                                     delete_hourly_income_service)
from uuid import UUID

router = APIRouter()

@router.get("/get_income_by_year")
async def get_income_by_year():
    return await get_income_by_year_service()

@router.get("/get_income_by_month/{year}")
async def get_income_by_month(year: int):
    return await get_income_by_month_service(year)

@router.post("/post_income")
async def put_income(payload: IncomeCreate):
    return await post_income_service(payload)

@router.delete("/delete_income/{income_date}")
async def soft_delete(payload: IncomeCreate):
    return await soft_delete_service(payload)

@router.get("/get_payment_fixed/{project_id}")
async def get_fix_income(project_id: UUID):
    return await get_fix_income_service(project_id)

@router.post("/post_payment_fixed/{project_id}")
async def insert_fix_income(project_id: UUID, payload: FixPaymentUpdate):
    return await insert_fix_income_service(project_id, payload)

@router.delete("/delete_payment_fixed/{project_id}")
async def delete_fix_income(project_id: UUID):
    return await delete_fix_income_service(project_id)

@router.get("/get_payment_hourly/{project_id}")
async def get_payment_hourly(project_id: UUID):
    return await get_hourly_income_service(project_id)

@router.post("/post_payment_hourly/{project_id}")
async def insert_hourly_income(project_id: UUID, payload: HourlyPaymentUpdate):
    return await insert_hourly_income_service(project_id, payload)

@router.delete("/delete_payment_hourly/{project_id}")
async def delete_hourly_income(project_id: UUID):
    return await delete_hourly_income_service(project_id)