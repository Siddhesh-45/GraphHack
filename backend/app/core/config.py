import sys
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, model_validator, ValidationError

ALLOWED_ENVS = {"development", "staging", "production", "test"}
ALLOWED_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_ENV: str = Field(default="development", description="Runtime environment: development | staging | production | test")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level: DEBUG | INFO | WARNING | ERROR | CRITICAL")
    BACKEND_HOST: str = Field(default="0.0.0.0", description="Backend binding host")
    BACKEND_PORT: int = Field(default=8000, description="Backend port")
    FRONTEND_PORT: int = Field(default=5173, description="Frontend port")
    
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
    MAX_CHUNKS_PER_DOCUMENT: int = Field(default=500)
    CHUNK_SIZE_TOKENS: int = Field(default=600)
    CHUNK_OVERLAP_TOKENS: int = Field(default=100)

    @field_validator("APP_ENV")
    @classmethod
    def validate_app_env(cls, v: str) -> str:
        clean = v.strip().lower()
        if clean not in ALLOWED_ENVS:
            raise ValueError(f"Invalid APP_ENV '{v}'. Allowed environments: {', '.join(sorted(ALLOWED_ENVS))}")
        return clean

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        clean = v.strip().upper()
        if clean not in ALLOWED_LOG_LEVELS:
            raise ValueError(f"Invalid LOG_LEVEL '{v}'. Allowed levels: {', '.join(sorted(ALLOWED_LOG_LEVELS))}")
        return clean

    @field_validator("BACKEND_PORT", "FRONTEND_PORT", "FALKORDB_PORT")
    @classmethod
    def validate_port_range(cls, v: int) -> int:
        if not (1 <= v <= 65535):
            raise ValueError(f"Port must be between 1 and 65535 (got {v})")
        return v

    @field_validator("MAX_UPLOAD_SIZE_MB", "MAX_CHUNKS_PER_DOCUMENT", "CHUNK_SIZE_TOKENS")
    @classmethod
    def validate_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError(f"Value must be greater than 0 (got {v})")
        return v

    @model_validator(mode="after")
    def validate_chunk_overlap(self) -> "Settings":
        if self.CHUNK_OVERLAP_TOKENS >= self.CHUNK_SIZE_TOKENS:
            raise ValueError(
                f"CHUNK_OVERLAP_TOKENS ({self.CHUNK_OVERLAP_TOKENS}) must be strictly less than "
                f"CHUNK_SIZE_TOKENS ({self.CHUNK_SIZE_TOKENS})"
            )
        return self

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


def load_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        error_lines = []
        for err in e.errors():
            loc = ".".join(str(p) for p in err.get("loc", []))
            msg = err.get("msg", "Invalid configuration")
            error_lines.append(f"  • {loc}: {msg}")
        formatted_error = (
            "\n" + "=" * 78 + "\n"
            "🚨 CRITICAL CONFIGURATION ERROR: Invalid or missing environment configuration\n"
            + "=" * 78 + "\n"
            + "\n".join(error_lines) + "\n\n"
            "Please check your .env file or environment variables against .env.example.\n"
            + "=" * 78 + "\n"
        )
        sys.stderr.write(formatted_error)
        raise SystemExit(1) from e


settings = load_settings()
