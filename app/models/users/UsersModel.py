from sqlmodel import SQLModel, Field
from typing import Optional
from ..company.company import Company
from ..departament.departament import Department

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    department_id: Optional[int] = Field(default=None, foreign_key="departments.id")
    company_id: Optional[int] = Field(default=None, foreign_key="companies.id")
    name: str
    email: str
    password_hash: str
    is_active: bool = True
    failed_attempts: int = 0
