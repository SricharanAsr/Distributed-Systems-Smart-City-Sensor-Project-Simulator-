import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import NoiseData


class NoiseSensor(BaseSensor):
    """
    Simulates acoustic noise levels in decibels (dB) for monitoring city noise pollution.
    Features Time-of-Day awareness:
    - Day (7-21): 60-120 dB
    - Night (22-6): 30-60 dB
    """

    def generate_data(self) -> Dict[str, Any]:
        data = NoiseData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            decibels=random.randint(30, 60) if (22 <= datetime.now().hour or datetime.now().hour <= 6) else random.randint(60, 120),
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()
