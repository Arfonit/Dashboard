from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class CompanyNameUpdate(BaseModel):
    unique_company_key: Optional[UUID] = uuid4()
    unique_group_key: Optional[UUID] = uuid4()
    company_name: str
    company_group: Optional[str] = None
    data_upload: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None