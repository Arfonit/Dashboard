from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class IncomeCreate(BaseModel):
    unique_income_key: Optional[UUID] = uuid4()
    income_date: datetime
    amount: float
    
class FixPaymentUpdate(BaseModel):
    unique_fix_payment_key: Optional[UUID] = uuid4()
    unique_project_key: Optional[UUID] = uuid4()
    project_budjet: float
    update_date: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    
class HourlyPaymentUpdate(BaseModel):
    unique_hourly_payment_key: Optional[UUID] = uuid4()
    unique_project_key: Optional[UUID] = uuid4()
    extra_work_price: float
    extra_work_hours: float
    update_date: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None