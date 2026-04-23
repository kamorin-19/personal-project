from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    aws_region: str = "ap-northeast-1"
    aws_access_key_id: str = "dummy"
    aws_secret_access_key: str = "dummy"
    dynamodb_endpoint_url: str | None = None

    allowed_origins: list[str] = ["http://localhost:5173"]

    # Google OAuth2
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:5173/auth/callback"

    # JWT セッション
    jwt_secret_key: str = "dev-secret-change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24


settings = Settings()
