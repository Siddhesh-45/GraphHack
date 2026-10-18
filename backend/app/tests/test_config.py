import pytest
from pydantic import ValidationError
from app.core.config import Settings, load_settings

def test_default_settings():
    settings = Settings()
    assert settings.APP_ENV in ["development", "staging", "production", "test"]
    assert settings.FALKORDB_PORT == 6379
    assert settings.FRONTEND_PORT == 5173
    assert settings.MAX_CHUNKS_PER_DOCUMENT == 500
    assert isinstance(settings.cors_origins_list, list)
    assert len(settings.cors_origins_list) > 0

def test_cors_origins_parsing():
    settings = Settings(CORS_ORIGINS="http://localhost:5173, http://example.com , ")
    origins = settings.cors_origins_list
    assert "http://localhost:5173" in origins
    assert "http://example.com" in origins
    assert len(origins) == 2

def test_invalid_app_env():
    with pytest.raises(ValidationError) as exc:
        Settings(APP_ENV="invalid_env_name")
    assert "Invalid APP_ENV" in str(exc.value)

def test_invalid_log_level():
    with pytest.raises(ValidationError) as exc:
        Settings(LOG_LEVEL="SUPER_VERBOSE")
    assert "Invalid LOG_LEVEL" in str(exc.value)

def test_invalid_port_range():
    with pytest.raises(ValidationError) as exc:
        Settings(BACKEND_PORT=99999)
    assert "Port must be between 1 and 65535" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        Settings(FALKORDB_PORT=0)
    assert "Port must be between 1 and 65535" in str(exc.value)

def test_invalid_chunk_overlap():
    with pytest.raises(ValidationError) as exc:
        Settings(CHUNK_SIZE_TOKENS=500, CHUNK_OVERLAP_TOKENS=600)
    assert "CHUNK_OVERLAP_TOKENS" in str(exc.value)

