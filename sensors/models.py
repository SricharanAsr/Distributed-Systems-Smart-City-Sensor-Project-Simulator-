from pydantic import BaseModel, Field
from typing import Literal


class BaseSensorData(BaseModel):
    sensorId: str
    city: str
    zone: str
    timestamp: str


class EnvironmentData(BaseSensorData):
    type: Literal["environment"] = "environment"
    temperature: float = Field(..., ge=-50.0, le=60.0)
    humidity: int = Field(..., ge=0, le=100)
    aqi: int = Field(..., ge=0, le=500)
    co2: int = Field(..., ge=0, le=2000)


class TrafficData(BaseSensorData):
    type: Literal["traffic"] = "traffic"
    vehicle_count: int = Field(..., ge=0)
    average_speed: float = Field(..., ge=0.0)


class WasteData(BaseSensorData):
    type: Literal["waste"] = "waste"
    fill_level: int = Field(..., ge=0, le=100)
    last_collected: str


class NoiseData(BaseSensorData):
    type: Literal["noise"] = "noise"
    decibels: int = Field(..., ge=0, le=200)


class EnergyData(BaseSensorData):
    type: Literal["energy"] = "energy"
    consumption_kw: float = Field(..., ge=0.0)
