from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    api_key: str

    model_config = SettingsConfigDict(env_file=(".env"), extra="allow")


class ImageFormatSettings(BaseSettings):
    single_image_format: str

    model_config = SettingsConfigDict(env_file=(".env"), extra="allow")
