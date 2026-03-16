from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.audit_schema import AuditLogResponse
from app.schemas.pagination_schema import PaginatedResponse
from app.models.audit_log import AuditLog

from app.utils.cache import cache

router = APIRouter()

@router.get("/", response_model=List[AuditLogResponse])
@cache(expire=3600)
def read_audit_logs(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(8, ge=1, le=500), # Default to 8
    current_user: Any = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve audit logs. (Admin only)
    """
    query = db.query(AuditLog)
    total = query.count()
    logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    
    import math
    return {
        "items": logs,
        "total": total,
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "size": limit,
        "pages": math.ceil(total / limit) if limit > 0 else 1
    }
