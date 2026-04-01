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


class WaterQualityData(BaseSensorData):
    type: Literal["water_quality"] = "water_quality"
    ph: float = Field(..., ge=0.0, le=14.0)
    turbidity: float = Field(..., ge=0.0, le=100.0)
    dissolved_oxygen: float = Field(..., ge=0.0, le=20.0)


class AirQualityData(BaseSensorData):
    type: Literal["air_quality"] = "air_quality"
    pm25: float = Field(..., ge=0.0, le=500.0)
    pm10: float = Field(..., ge=0.0, le=500.0)
    no2: float = Field(..., ge=0.0, le=500.0)
    o3: float = Field(..., ge=0.0, le=500.0)


class ParkingData(BaseSensorData):
    type: Literal["parking"] = "parking"
    total_spots: int = Field(..., ge=0)
    occupied_spots: int = Field(..., ge=0)
    available_spots: int = Field(..., ge=0)


class StreetLightData(BaseSensorData):
    type: Literal["streetlight"] = "streetlight"
    status: Literal["On", "Off", "Dimmed"]
    energy_usage_kwh: float = Field(..., ge=0.0)


