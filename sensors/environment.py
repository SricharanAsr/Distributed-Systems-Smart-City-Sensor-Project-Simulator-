import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import EnvironmentData

class EnvironmentSensor(BaseSensor):
    """
    Simulates environmental factors such as temperature, humidity, and air quality.
    """
    def generate_data(self) -> Dict[str, Any]:
        data = EnvironmentData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            temperature=round(random.uniform(25, 40), 2),
            humidity=random.randint(40, 80),
            aqi=random.randint(50, 300),
            co2=random.randint(350, 500),
            timestamp=datetime.now().isoformat()
        )
        return data.model_dump()
