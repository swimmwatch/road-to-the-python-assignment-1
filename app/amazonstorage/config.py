from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioSettings(BaseSettings):
    endpoint: str
    root_user: str
    access_key: str
    secret_key: str
    bucket_name: str

    model_config = SettingsConfigDict(
        env_prefix="minio_", env_file=(".env"), extra="allow"
    )
