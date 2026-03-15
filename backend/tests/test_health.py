import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_health_check_success():
    """Test health check when all services are up."""
    with patch("app.api.routes.health.Session") as mock_db, \
         patch("app.api.routes.health.RedisService") as mock_redis, \
         patch("app.api.routes.health.celery_app") as mock_celery:
        
        # DB mock
        mock_db_instance = MagicMock()
        mock_db.return_value = mock_db_instance
        
        # Redis mock
        mock_redis_instance = MagicMock()
        mock_redis_instance.ping.return_value = True
        mock_redis.return_value = mock_redis_instance
        
        # Celery mock
        mock_celery.control.inspect().ping.return_value = {"celery@worker": "pong"}
        
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "up"
        assert data["redis"] == "up"
        assert data["celery"] == "up"

def test_health_check_partial_failure():
    """Test health check when Redis is down."""
    with patch("app.api.routes.health.Session") as mock_db, \
         patch("app.api.routes.health.RedisService") as mock_redis, \
         patch("app.api.routes.health.celery_app") as mock_celery:
        
        # DB mock
        mock_db_instance = MagicMock()
        mock_db.return_value = mock_db_instance
        
        # Redis mock (Simulate Ping failure)
        mock_redis_instance = MagicMock()
        mock_redis_instance.ping.return_value = False
        mock_redis.return_value = mock_redis_instance
        
        # Celery mock
        mock_celery.control.inspect().ping.return_value = {"celery@worker": "pong"}
        
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200 # App is alive, but summary might show issue
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["redis"] == "down"
捉
