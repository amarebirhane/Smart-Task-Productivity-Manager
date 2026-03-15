from typing import Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api import deps
from app.services.redis_service import redis_service
from app.core.celery_app import celery_app

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    components: Dict[str, str]

@router.get("", response_model=HealthResponse, summary="Check system health")
def health_check(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Check the health of the application and its core dependencies.
    """
    overall_status = "healthy"
    components = {
        "database": "unhealthy",
        "redis": "unhealthy",
        "celery": "unhealthy"
    }
    
    # 1. Check Database
    try:
        db.execute(text("SELECT 1"))
        components["database"] = "healthy"
    except Exception as e:
        overall_status = "unhealthy"
        components["database"] = f"error: {str(e)}"

    # 2. Check Redis
    if redis_service.client:
        try:
            if redis_service.client.ping():
                components["redis"] = "healthy"
        except Exception as e:
            overall_status = "unhealthy"
            components["redis"] = f"error: {str(e)}"
    
    # 3. Check Celery (Active Workers)
    try:
        insp = celery_app.control.inspect()
        stats = insp.stats()
        if stats:
            components["celery"] = "healthy"
        else:
            components["celery"] = "no_workers_running"
    except Exception as e:
        components["celery"] = f"error: {str(e)}"

    return {
        "status": overall_status,
        "components": components
    }
