from fastapi import APIRouter
from uuid import UUID
from backend.schemas.payment_schemas import (FactPaymentUpdate)
from services.payment_service import (get_fact_payment_service,
                                      insert_fact_payment_service,
                                      delete_fact_payment_service,
                                      get_total_fact_payment_service)


router = APIRouter()

@router.get("/get_total_fact_payment")
async def get_total_fact_payment():
    return await get_total_fact_payment_service()

@router.get("/get_fact_payment/{project_id}")
async def get_fact_payment(project_id: UUID):
    return await get_fact_payment_service(project_id)

@router.post("/post_fact_payment/{project_id}")
async def insert_fact_payment(project_id: UUID, payload: FactPaymentUpdate):
    return await insert_fact_payment_service(project_id, payload)

@router.delete("/delete_fact_payment/{project_id}")
async def delete_fact_payment(project_id: UUID):
    return await delete_fact_payment_service(project_id)

