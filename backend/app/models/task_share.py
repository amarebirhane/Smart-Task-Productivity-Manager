import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class TaskShare(Base):
    __tablename__ = "task_shares"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Permission level: "read" or "write"
    permission = Column(String, default="read", nullable=False) 
    
    shared_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", backref="shares")
    user = relationship("User", backref="shared_tasks")
