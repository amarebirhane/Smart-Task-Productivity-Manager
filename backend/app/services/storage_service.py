import boto3
import logging
from botocore.exceptions import ClientError
from typing import Optional, Union
from app.core.config import settings
import io

logger = logging.getLogger("app.storage")

class StorageService:
    def __init__(self):
        self.s3_client = None
        if all([settings.S3_ENDPOINT_URL, settings.S3_ACCESS_KEY, settings.S3_SECRET_KEY]):
            try:
                self.s3_client = boto3.client(
                    "s3",
                    endpoint_url=settings.S3_ENDPOINT_URL,
                    aws_access_key_id=settings.S3_ACCESS_KEY,
                    aws_secret_access_key=settings.S3_SECRET_KEY,
                    region_name="us-east-1" # MinIO default
                )
                # Ensure bucket exists
                self._ensure_bucket()
            except Exception as e:
                logger.error(f"Failed to initialize S3 client: {e}")

    def _ensure_bucket(self):
        try:
            self.s3_client.head_bucket(Bucket=settings.S3_BUCKET)
        except ClientError:
            try:
                self.s3_client.create_bucket(Bucket=settings.S3_BUCKET)
                logger.info(f"Created bucket: {settings.S3_BUCKET}")
            except Exception as e:
                logger.error(f"Failed to create bucket: {e}")

    def upload_file(self, file_content: bytes, object_name: str, content_type: str) -> bool:
        """Upload a file to the S3 bucket."""
        if not self.s3_client:
            logger.warning("S3 client not initialized. Skipping upload.")
            return False
        
        try:
            self.s3_client.put_object(
                Bucket=settings.S3_BUCKET,
                Key=object_name,
                Body=file_content,
                ContentType=content_type
            )
            return True
        except ClientError as e:
            logger.error(f"S3 upload error: {e}")
            return False

    def get_presigned_url(self, object_name: str, expiration: int = 3600) -> Optional[str]:
        """Generate a presigned URL to share an S3 object."""
        if not self.s3_client:
            return None
        
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.S3_BUCKET, 'Key': object_name},
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            return None

    def delete_file(self, object_name: str) -> bool:
        """Delete an object from the S3 bucket."""
        if not self.s3_client:
            return False
        
        try:
            self.s3_client.delete_object(Bucket=settings.S3_BUCKET, Key=object_name)
            return True
        except ClientError as e:
            logger.error(f"S3 delete error: {e}")
            return False

storage_service = StorageService()
