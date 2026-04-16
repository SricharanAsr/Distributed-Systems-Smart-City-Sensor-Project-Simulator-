import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import WasteData


class WasteSensor(BaseSensor):
    def __init__(self, config):
        super().__init__(config)
        self._current_fill = random.randint(0, 50)

    """
    Simulates waste management metrics such as bin fill levels.
    """

    def generate_data(self) -> Dict[str, Any]:
        data = WasteData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            fill_level=random.randint(0, 100),
            last_collected=datetime.now().isoformat(),
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()
