import requests
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger('SmartCitySimulator')

class BaseSensor(ABC):
    """
    Abstract base class for all smart city sensors.
    Common logic for configuration and data transmission.
    """
    def __init__(self, config):
        self.config = config
        self.backend_url = config.get("backend_url")
        self.city = config.get("city")
        self.zones = config.get("zones")
        self.sensor_ids = config.get("sensor_ids")

    @abstractmethod
    def generate_data(self):
        pass

    def send_data(self):
        data = self.generate_data()
        try:
            response = requests.post(self.backend_url, json=data)
            logger.info(f"[{self.__class__.__name__}] Sent Data: {data}")
            logger.info(f"[{self.__class__.__name__}] Server Response: {response.text}")
        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] Error sending data: {e}")
