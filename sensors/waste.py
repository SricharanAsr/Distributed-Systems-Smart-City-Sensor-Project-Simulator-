import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor

class WasteSensor(BaseSensor):
    """
    Simulates waste management metrics such as bin fill levels.
    """
    def generate_data(self) -> Dict[str, Any]:
        return {
            "sensorId": random.choice(self.sensor_ids),
            "city": self.city,
            "zone": random.choice(self.zones),
            "fill_level": random.randint(0, 100),
            "last_collected": datetime.now().isoformat(),
            "timestamp": datetime.now().isoformat(),
            "type": "waste"
        }
