import os
import subprocess
import logging
from datetime import datetime
from typing import List, Optional
from app.core.config import settings

logger = logging.getLogger("app.backup")

class BackupService:
    def __init__(self):
        self.backup_dir = settings.BACKUP_DIR
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_backup(self) -> Optional[str]:
        """
        Creates a database backup using pg_dump.
        Returns the path to the created backup file or None if it fails.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{timestamp}.sql"
        filepath = os.path.join(self.backup_dir, filename)

        # Build the pg_dump command
        # Format: pg_dump -U user -h host -p port dbname > filepath
        # We'll use the environment variable PGPASSWORD to provide the password securely
        env = os.environ.copy()
        env["PGPASSWORD"] = settings.POSTGRES_PASSWORD

        try:
            command = [
                "pg_dump",
                "-U", settings.POSTGRES_USER,
                "-h", settings.POSTGRES_SERVER,
                "-p", str(settings.POSTGRES_PORT),
                "-F", "c",  # Custom format (compressed, for pg_restore)
                "-f", filepath,
                settings.POSTGRES_DBS
            ]
            
            logger.info(f"Starting database backup: {filename}")
            result = subprocess.run(command, env=env, check=True, capture_output=True, text=True)
            logger.info(f"Backup created successfully: {filepath}")
            return filepath
        except subprocess.CalledProcessError as e:
            logger.error(f"Backup failed: {e.stderr}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during backup: {e}")
            return None

    def list_backups(self) -> List[str]:
        """Lists all available backup files."""
        if not os.path.exists(self.backup_dir):
            return []
        return sorted([f for f in os.listdir(self.backup_dir) if f.endswith(".sql")], reverse=True)

    def delete_backup(self, filename: str) -> bool:
        """Deletes a backup file."""
        filepath = os.path.join(self.backup_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

backup_service = BackupService()
