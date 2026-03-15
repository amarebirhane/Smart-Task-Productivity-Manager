from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api import deps
from app.services.redis_service import redis_service
from app.core.celery_app import celery_app

router = APIRouter()

@router.get("", summary="Check system health")
def health_check(
    db: Session = Depends(deps.get_db)
) -> Dict[str, Any]:
    """
    Check the health of the application and its core dependencies.
    """
    health_status = {
        "status": "healthy",
        "components": {
            "database": "unhealthy",
            "redis": "unhealthy",
            "celery": "unhealthy"
        }
    }
    
    # 1. Check Database
    try:
        db.execute(text("SELECT 1"))
        health_status["components"]["database"] = "healthy"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["components"]["database"] = f"error: {str(e)}"

    # 2. Check Redis
    if redis_service.client:
        try:
            if redis_service.client.ping():
                health_status["components"]["redis"] = "healthy"
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["components"]["redis"] = f"error: {str(e)}"
    
    # 3. Check Celery (Active Workers)
    try:
        insp = celery_app.control.inspect()
        stats = insp.stats()
        if stats:
            health_status["components"]["celery"] = "healthy"
        else:
            health_status["components"]["celery"] = "no_workers_running"
            # We don't mark the whole system unhealthy if only background workers are down, 
            # unless background tasks are critical for the current request.
    except Exception as e:
        health_status["components"]["celery"] = f"error: {str(e)}"

    return health_status
