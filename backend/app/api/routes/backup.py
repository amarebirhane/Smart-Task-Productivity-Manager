from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import FileResponse
from typing import Any, List
import os

from app.api import deps
from app.services.backup_service import backup_service
from app.core.config import settings

router = APIRouter()

@router.post("/create", summary="Create a new database backup")
def create_backup(
    current_user: Any = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Create a new database backup. Only superusers can trigger backups.
    """
    filepath = backup_service.create_backup()
    if not filepath:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create database backup"
        )
    return {"msg": "Backup created successfully", "filename": os.path.basename(filepath)}

@router.get("/list", response_model=List[str], summary="List all backups")
def list_backups(
    current_user: Any = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    List all available database backup files.
    """
    return backup_service.list_backups()

@router.get("/download/{filename}", summary="Download a backup file")
def download_backup(
    filename: str,
    current_user: Any = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Download a specific database backup file.
    """
    filepath = os.path.join(settings.BACKUP_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backup file not found"
        )
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/octet-stream"
    )

@router.delete("/{filename}", summary="Delete a backup file")
def delete_backup(
    filename: str,
    current_user: Any = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Delete a database backup file.
    """
    if backup_service.delete_backup(filename):
        return {"msg": f"Backup {filename} deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Backup file not found"
    )
