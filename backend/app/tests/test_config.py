from app.core.config import Settings

def test_default_settings():
    settings = Settings()
    assert settings.APP_ENV in ["development", "staging", "production", "test"]
    assert settings.FALKORDB_PORT == 6379
    assert isinstance(settings.cors_origins_list, list)
    assert len(settings.cors_origins_list) > 0

def test_cors_origins_parsing():
    settings = Settings(CORS_ORIGINS="http://localhost:5173, http://example.com , ")
    origins = settings.cors_origins_list
    assert "http://localhost:5173" in origins
    assert "http://example.com" in origins
    assert len(origins) == 2
