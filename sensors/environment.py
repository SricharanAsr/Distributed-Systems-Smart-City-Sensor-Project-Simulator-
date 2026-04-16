import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import EnvironmentData


class EnvironmentSensor(BaseSensor):
    """
    Simulates environmental factors.
    Units:
    - Temperature: Celsius
    - Humidity: % (0-100)
    - AQI: Index
    - CO2: ppm
    """

    def generate_data(self) -> Dict[str, Any]:
        data = EnvironmentData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            temperature=max(-10.0, min(50.0, round(random.uniform(25, 40), 2))),
            humidity=max(0, min(100, random.randint(40, 80))),
            aqi=random.randint(50, 300),
            co2=random.randint(350, 500),
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()

# Timezone fallback
