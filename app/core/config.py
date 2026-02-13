from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_dev_token: str = "dev-agent-token"

settings = Settings()

