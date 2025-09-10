from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Document(SQLModel, table=True):
    __tablename__ = "documents"  

    id: Optional[int] = Field(default=None, primary_key=True)

    department_id: Optional[int] = None
    uploaded_by: int                     
    doc_type_id: Optional[int] = None
    company_id: Optional[int] = None

    title: str                             
    original_filename: str                

    uploaded_at: Optional[datetime] = None  
    processed: Optional[int] = 0           

class DocumentCreate(BaseModel):
    department_id: int
    uploaded_by: int
    doc_type_id: int
    company_id: int
    title: str