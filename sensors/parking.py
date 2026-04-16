import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import ParkingData

class ParkingSensor(BaseSensor):
    """
    Simulates parking availability metrics for a smart city environment.
    """

    def generate_data(self) -> Dict[str, Any]:
        total_spots = random.randint(50, 500)
        occupied_spots = random.randint(0, total_spots)
        
        data = ParkingData(
            sensorId=random.choice(self.sensor_ids),
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
