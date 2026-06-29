from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID, uuid4
from typing import Optional
    
    
class StartProjectDateUpdate(BaseModel):
    unique_project_date_key: Optional[UUID] = uuid4()
    unique_project_key: Optional[UUID] = uuid4()
    project_date: date
    update_date: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    
class ProjectTypeUpdate(BaseModel):
    unique_project_type_key: Optional[UUID] = None
    project_type: str
    update_date: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    

class ProjectUpdate(BaseModel):
    unique_company_key: Optional[UUID] = uuid4()
    company_name: str
    unique_income_project_key: Optional[UUID] = uuid4()
    project_type: str
    unique_comment_key: Optional[UUID] = uuid4()
    comment: str
    unique_income_project_key: Optional[UUID] = uuid4()
    fact_payment: str
    unique_fix_payment_key: Optional[UUID] = uuid4()
    project_budjet: float
    unique_hourly_payment_key: Optional[UUID] = uuid4()
    extra_work_price: float
    extra_work_hours: float
    unique_project_date_key: Optional[UUID] = uuid4()
    project_date: date
    
    
class Project(BaseModel):
    project_date: date
    company_name: str
    project_type: str
    comment: str
    project_budjet: float
    extra_work_price: float
    extra_work_hours: float
    fact_payment: float

class KeyTable(BaseModel):
    unique_project_key: Optional[UUID] = None
    unique_company_key: Optional[UUID] = None
    unique_project_type_key: Optional[UUID] = None
    unique_comment_key: Optional[UUID] = None
    unique_income_project_key: Optional[UUID] = None
    unique_fix_payment_key: Optional[UUID] = None
    unique_hourly_payment_key: Optional[UUID] = None
    unique_project_date_key: Optional[UUID] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None