import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import PedestrianData


class PedestrianSensor(BaseSensor):
    """
    Simulates pedestrian traffic monitoring for urban planning and safety.
    """

    def generate_data(self) -> Dict[str, Any]:
        data = PedestrianData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            count=random.randint(0, 50),
            direction=random.choice(["Inbound", "Outbound", "Cross"]),
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()
