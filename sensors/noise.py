import random
from datetime import datetime
from .base import BaseSensor

class NoiseSensor(BaseSensor):
    """
    Simulates acoustic noise levels in decibels (dB) for monitoring city noise pollution.
    """
    def generate_data(self):
        return {
            "sensorId": random.choice(self.sensor_ids),
            "city": self.city,
            "zone": random.choice(self.zones),
            "decibels": random.randint(40, 120),
            "timestamp": datetime.now().isoformat(),
            "type": "noise"
        }
