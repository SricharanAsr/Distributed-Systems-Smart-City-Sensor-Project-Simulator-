import random
import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import WaterQualityData


class WaterQualitySensor(BaseSensor):
    """
    Simulates a water quality sensor measuring pH, turbidity, and dissolved oxygen.
    """

    def generate_data(self) -> Dict[str, Any]:
        sensor_id = random.choice(self.sensor_ids)
        zone = random.choice(self.zones)

        data = WaterQualityData(
            sensorId=sensor_id,
            city=self.city,
            zone=zone,
            timestamp=datetime.datetime.now().isoformat(),
            ph=round(random.uniform(6.5, 8.5), 2),
            turbidity=round(random.uniform(0.0, 5.0), 2),
            dissolved_oxygen=round(random.uniform(5.0, 12.0), 2),
        )
        return data.model_dump()
