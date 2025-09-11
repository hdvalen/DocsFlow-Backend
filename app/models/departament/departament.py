from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Department(SQLModel, table=True):
    __tablename__ = "departments"

    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companies.id")
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
