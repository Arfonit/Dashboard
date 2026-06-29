from pydantic import BaseModel
from datetime import date
from uuid import UUID

class Dashboard(BaseModel):
    unique_project_key: UUID
    project_date: date
    company_name: str
    project_type: str
    comment: str
    project_budjet: float
    extra_work_price: float
    extra_work_hours: float
    total_extra_pay:float
    fact_payment: float
    percent_paid: float