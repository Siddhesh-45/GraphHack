from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any

class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Status string: healthy, degraded, or unhealthy")
    version: str = Field(default="1.0.0", description="Company Brain build version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    environment: str = Field(default="development")
    falkordb: Dict[str, Any] = Field(default_factory=dict)
