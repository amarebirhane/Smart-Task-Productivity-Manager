import pytest
from unittest.mock import MagicMock, patch
from io import BytesIO
from app.services.storage_service import StorageService

class TestStorageService:
    @patch("boto3.client")
    def test_upload_file_success(self, mock_boto_client):
        # Setup mock
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        # Execute
        service = StorageService()
        file_obj = BytesIO(b"test content")
        result = service.upload_file(file_obj, "test.txt")
        
        # Verify
        assert result is not None
        assert result.startswith("taskmind/test.txt")
        mock_s3.put_object.assert_called_once()

    @patch("boto3.client")
    def test_get_presigned_url(self, mock_boto_client):
        # Setup mock
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.generate_presigned_url.return_value = "https://mock-url.com"
        
        # Execute
        service = StorageService()
        url = service.get_presigned_url("test.txt")
        
        # Verify
        assert url == "https://mock-url.com"
        mock_s3.generate_presigned_url.assert_called_once_with(
            "get_object",
            Params={"Bucket": "task-attachments", "Key": "test.txt"},
            ExpiresIn=3600
        )

    @patch("boto3.client")
    def test_delete_file_success(self, mock_boto_client):
        # Setup mock
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        # Execute
        service = StorageService()
        result = service.delete_file("test.txt")
        
        # Verify
        assert result is True
        mock_s3.delete_object.assert_called_once_with(
            Bucket="task-attachments",
            Key="test.txt"
        )
捉
