import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=True) # None for anonymous actions
    username = Column(String, index=True, nullable=True)
    action = Column(String, index=True, nullable=False) # login, logout, create_task, etc.
    target_type = Column(String, index=True, nullable=True) # task, user, setting, etc.
    target_id = Column(String, index=True, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
