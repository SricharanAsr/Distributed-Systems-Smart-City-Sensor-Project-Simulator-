import requests
import logging
from typing import Dict, Any, List
from abc import ABC, abstractmethod

logger = logging.getLogger("SmartCitySimulator")


class BaseSensor(ABC):
    """
    Abstract base class for all smart city sensors.
    Common logic for configuration and data transmission.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.backend_url: str = config.get("backend_url", "")
        self.city: str = config.get("city", "")
        self.zones: List[str] = config.get("zones", [])
        self.sensor_ids: List[str] = config.get("sensor_ids", [])

    @abstractmethod
    def generate_data(self) -> Dict[str, Any]:
        pass

    def send_data(self) -> None:
        data = self.generate_data()
        try:
            response = requests.post(self.backend_url, json=data)
            logger.info(f"[{self.__class__.__name__}] Sent Data: {data}")
            logger.info(f"[{self.__class__.__name__}] Server Response: {response.text}")
        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] Error sending data: {e}")
