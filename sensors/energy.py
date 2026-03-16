import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor

class EnergySensor(BaseSensor):
    """
    Simulates power consumption metrics for a city area in kilowatts (kW).
    """
    def generate_data(self) -> Dict[str, Any]:
        return {
            "sensorId": random.choice(self.sensor_ids),
            "city": self.city,
            "zone": random.choice(self.zones),
            "consumption_kw": round(random.uniform(10.0, 500.0), 2),
            "timestamp": datetime.now().isoformat(),
            "type": "energy"
        }
