import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import NoiseData

class NoiseSensor(BaseSensor):
    """
    Simulates acoustic noise levels in decibels (dB) for monitoring city noise pollution.
    """
    def generate_data(self) -> Dict[str, Any]:
        data = NoiseData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            decibels=random.randint(40, 120),
            timestamp=datetime.now().isoformat()
        )
        return data.model_dump()
