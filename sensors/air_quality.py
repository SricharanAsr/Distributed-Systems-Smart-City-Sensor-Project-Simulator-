import random
import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import AirQualityData


class AirQualitySensor(BaseSensor):
    """
    Simulates an air quality sensor measuring PM2.5, PM10, NO2, and O3.
    Uses a programmatic correlation model (PM10 = PM2.5 * 1.2-1.8) for realistic data generation.
    """

    def generate_data(self) -> Dict[str, Any]:
        sensor_id = random.choice(self.sensor_ids)
        zone = random.choice(self.zones)

        data = AirQualityData(
            sensorId=sensor_id,
            city=self.city,
            zone=zone,
            timestamp=datetime.datetime.now().isoformat(),
            pm25=round(random.uniform(0.0, 150.0), 2),
            pm10=round(random.uniform(0.0, 150.0) * random.uniform(1.2, 1.8), 2),
            no2=round(random.uniform(0.0, 100.0), 2),
            o3=round(random.uniform(0.0, 100.0), 2),
        )
        return data.model_dump()
