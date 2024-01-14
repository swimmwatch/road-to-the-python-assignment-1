from minio import Minio

from .config import MinioSettings

minio_client = Minio(
    endpoint=MinioSettings().endpoint,
    access_key=MinioSettings().access_key,
    secret_key=MinioSettings().secret_key,
    secure=False,
)


bucket_name = MinioSettings().bucket_name
