from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    language = Column(String(50), default="unknown")
    document_type = Column(String(100), default="Other")
    summary = Column(Text, default="")
    important_clauses = Column(Text, default="")
    compliance_dates = Column(Text, default="")
    checklist = Column(Text, default="[]")
    priority = Column(String(20), default="Medium")
    created_at = Column(DateTime, default=datetime.utcnow)

