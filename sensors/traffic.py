import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor

class TrafficSensor(BaseSensor):
    """
    Simulates traffic flow data including vehicle counts and average speeds.
    """
    def generate_data(self) -> Dict[str, Any]:
        return {
            "sensorId": random.choice(self.sensor_ids),
            "city": self.city,
            "zone": random.choice(self.zones),
            "vehicle_count": random.randint(0, 100),
            "average_speed": round(random.uniform(10, 60), 2),
            "timestamp": datetime.now().isoformat(),
            "type": "traffic"
        }
