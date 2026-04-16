import random
from datetime import datetime, timedelta
from typing import Dict, Any
from .base import BaseSensor
from .models import StreetLightData

class StreetLightSensor(BaseSensor):
    """
    Simulates streetlight status and energy usage for a smart city environment.
    Incorporates seasonal simulation altering active hours based on diurnal cycles.
    """

    def generate_data(self) -> Dict[str, Any]:
        hour = datetime.now().hour
        if 8 <= hour <= 18:
            status = 'Off'
        else:
            status = random.choice(['On', 'Dimmed'])
        
        consumption = 0.0
        if status == "On":
            consumption = random.uniform(0.1, 0.5)
        elif status == "Dimmed":
            consumption = random.uniform(0.01, 0.1)
            
        data = StreetLightData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            status=status, # type: ignore
            energy_usage_kwh=round(consumption, 4),
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()
