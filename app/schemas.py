from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    language: str
    document_type: str
    summary: str
    important_clauses: str
    compliance_dates: str
    priority: str
    checklist: str
    created_at: datetime

    class Config:
        from_attributes = True
