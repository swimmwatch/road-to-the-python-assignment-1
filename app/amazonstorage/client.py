from minio import Minio

from .config import MinioSettings

settings = MinioSettings()
minio_client = Minio(
    endpoint=settings.endpoint,
    access_key=settings.access_key,
    secret_key=settings.secret_key,
    secure=False,
)


bucket_name = settings.bucket_name
