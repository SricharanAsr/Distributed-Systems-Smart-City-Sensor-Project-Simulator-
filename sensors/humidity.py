import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import HumidityData


class HumiditySensor(BaseSensor):
    """
    Simulates high-precision humidity and dew point data for climate monitoring.
    """

    def generate_data(self) -> Dict[str, Any]:
        data = HumidityData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            relative_humidity=round(random.uniform(30, 90), 2),
            dew_point=round(random.uniform(5, 25), 2),
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()
