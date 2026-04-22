from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional


class AppConfig(BaseModel):
    """Schema for the Smart City Simulator configuration."""
    
    backend_url: str = Field(
        ..., 
        description="The API endpoint for data ingestion"
    )
    city: str = Field(
        "UnknownCity", 
        description="Default city for sensor data"
    )
    zones: List[str] = Field(
        default_factory=lambda: ["ZoneA"], 
        description="List of simulation zones"
    )
    sensor_ids: List[str] = Field(
        default_factory=lambda: ["S1"], 
        description="List of available sensor IDs"
    )
    interval: int = Field(
        5, 
        ge=1, 
        description="Simulation interval in seconds"
    )
    dry_run: bool = Field(
        False, 
        description="If true, logs data instead of sending API calls"
    )
    max_retries: int = Field(
        3, 
        ge=0, 
        description="Number of retries for failed transmissions"
    )
    json_logging: bool = Field(
        False, 
        description="Enable structured JSON logging"
    )
    cache_dir: str = Field(
        "data_cache", 
        description="Directory for local data persistence"
    )
    initial_battery: int = Field(
        100, 
        ge=0, 
        le=100, 
        description="Starting level for BatterySensors"
    )
