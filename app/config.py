from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email settings
    EMAIL_FROM: str
    EMAIL_SERVER: str
    EMAIL_PORT: int
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
