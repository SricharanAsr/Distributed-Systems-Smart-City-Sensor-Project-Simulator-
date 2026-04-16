import random
import hashlib
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import ParkingData

class ParkingSensor(BaseSensor):
    def _get_total_spots(self, sensor_id: str) -> int:
        h = int(hashlib.md5(sensor_id.encode()).hexdigest(), 16)
        return 50 + (h % 450)

    """
    Simulates parking availability metrics for a smart city environment.
    """

    def generate_data(self) -> Dict[str, Any]:
        sensor_id = random.choice(self.sensor_ids)
        total_spots = self._get_total_spots(sensor_id)
        occupied_spots = max(0, min(total_spots, random.randint(0, total_spots)))
        
        data = ParkingData(
            sensorId=sensor_id,
            city=self.city,
            zone=random.choice(self.zones),
            total_spots=total_spots,
            occupied_spots=occupied_spots,
            available_spots=total_spots - occupied_spots,
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()

# Debug trace support

# Boundary validation
