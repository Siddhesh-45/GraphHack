from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = Field(default="development")
    LOG_LEVEL: str = Field(default="INFO")
    BACKEND_HOST: str = Field(default="0.0.0.0")
    BACKEND_PORT: int = Field(default=8000)
    
    CORS_ORIGINS: str = Field(default="http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173")
    
    FALKORDB_HOST: str = Field(default="localhost")
    FALKORDB_PORT: int = Field(default=6379)
    FALKORDB_PASSWORD: str = Field(default="")
    FALKORDB_GRAPH: str = Field(default="company_brain")
    FALKORDB_MAX_CONNECTIONS: int = Field(default=20)
    
    GOOGLE_API_KEY: str = Field(default="")
    LLM_MODEL: str = Field(default="gemini-1.5-flash")
    EMBEDDING_MODEL: str = Field(default="text-embedding-004")
    
    MAX_UPLOAD_SIZE_MB: int = Field(default=25)
    CHUNK_SIZE_TOKENS: int = Field(default=600)
    CHUNK_OVERLAP_TOKENS: int = Field(default=100)

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
