import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import PressureData


class PressureSensor(BaseSensor):
    """
    Simulates atmospheric pressure sensors for weather station monitoring.
    """

    def generate_data(self) -> Dict[str, Any]:
        pressure = round(random.uniform(980.0, 1030.0), 2)
        # Simplify altitude calculation for simulation
        altitude = round((1013.25 - pressure) * 9, 2) 
        
        data = PressureData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            atmospheric_pressure=pressure,
            altitude_equivalent=max(0.0, altitude),
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()
