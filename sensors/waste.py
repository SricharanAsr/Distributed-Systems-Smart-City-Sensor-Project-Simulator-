import random
from datetime import datetime
from typing import Dict, Any
from .base import BaseSensor
from .models import WasteData


class WasteSensor(BaseSensor):
    def __init__(self, config):
        super().__init__(config)
        self._current_fill = random.randint(0, 50)
        self._last_collected_ts = datetime.now().isoformat()

    """
    Simulates waste management metrics such as bin fill levels.
    Algorithmic stateful tracking maintains current fill conditions globally.
    """

    def generate_data(self) -> Dict[str, Any]:
        self._current_fill += random.randint(5, 15)
        if self._current_fill >= 100:
            self._current_fill = 0
            self._last_collected_ts = datetime.now().isoformat()
        data = WasteData(
            sensorId=random.choice(self.sensor_ids),
            city=self.city,
            zone=random.choice(self.zones),
            fill_level=self._current_fill,

            last_collected=self._last_collected_ts,
            timestamp=datetime.now().isoformat(),
        )
        return data.model_dump()
