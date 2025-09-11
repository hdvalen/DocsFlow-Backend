from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentResponse(BaseModel):
    id: int
    department_id: Optional[int]
    doc_type_id: Optional[int]
    company_id: Optional[int]
    title: str
    original_filename: str
    uploaded_at: datetime
    processed: bool
