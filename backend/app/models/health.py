from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Dict, Any

class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Status string: healthy, degraded, or unhealthy")
    version: str = Field(default="1.0.0", description="Company Brain build version")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    environment: str = Field(default="development", description="Active runtime environment (development, production)")
    falkordb: Dict[str, Any] = Field(default_factory=dict, description="FalkorDB connection and node count telemetry")
