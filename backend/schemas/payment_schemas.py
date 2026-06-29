from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class FactPaymentUpdate(BaseModel):
    unique_income_project_key: Optional[UUID] = uuid4()
    unique_project_key: Optional[UUID] = uuid4()
    fact_payment: float
    update_date: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None