import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import BatteryData


class BatterySensor(BaseSensor):
    """
    Simulates the battery health and depletion levels of an IoT sensor node.
    This is a stateful sensor where the level gradually decreases.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.current_level = config.get("initial_battery", 100)
        self.voltage_base = 3.7

    def generate_data(self) -> Dict[str, Any]:
        # Simulate gradual drainage
        drain = random.uniform(0.1, 0.5)
        self.current_level = max(0, self.current_level - drain)
        
        # Calculate a realistic voltage based on level
        voltage = round(self.voltage_base * (self.current_level / 100) + random.uniform(-0.05, 0.05), 2)
        
        data = BatteryData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            level=int(self.current_level),
            voltage=max(0.0, voltage),
            is_charging=False,
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()
