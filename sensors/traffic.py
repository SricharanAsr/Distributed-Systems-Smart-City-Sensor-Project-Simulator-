import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import TrafficData


class TrafficSensor(BaseSensor):
    """
    Simulates traffic flow data including vehicle counts and average speeds.
    """

    def generate_data(self) -> Dict[str, Any]:
        data = TrafficData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            vehicle_count=max(0, random.randint(0, 100)),
            average_speed=max(0.0, round(random.uniform(10, 60), 2)),
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()
