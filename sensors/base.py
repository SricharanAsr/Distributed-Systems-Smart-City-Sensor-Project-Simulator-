import requests
import logging
from typing import Dict, Any, List
from abc import ABC, abstractmethod

logger = logging.getLogger("SmartCitySimulator")


class BaseSensor(ABC):
    """
    Abstract base class for all smart city sensors.
    Provides the core threading execution model, HTTP session management,
    and lifecycle handling for individual sensor implementations.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.backend_url: str = config.get("backend_url", "")
        self.city: str = config.get("city", "")
        self.zones: List[str] = config.get("zones", [])
        self.sensor_ids: List[str] = config.get("sensor_ids", [])
        self.dry_run: bool = config.get("dry_run", False)
        self.max_retries = 3
        
        # Statistics
        self.total_sent: int = 0
        self.total_failed: int = 0
        
        # Optimize HTTP connections

        self.session = requests.Session()
        
    def __del__(self) -> None:
        if hasattr(self, 'session'):
            self.session.close()

    @abstractmethod

    def generate_data(self) -> Dict[str, Any]:
        pass

    def _execute_request_with_retry(self, data: Dict[str, Any]) -> requests.Response:
        return self.session.post(self.backend_url, json=data, timeout=5)

    def send_data(self) -> None:
        import time
        data = self.generate_data()
        
        if self.dry_run:
            logger.info(f"[DRY-RUN] {self.__class__.__name__} Data: {data}")
            return
        
        for attempt in range(self.max_retries):

            try:
                response = self._execute_request_with_retry(data)
                response.raise_for_status()

                logger.debug(f"[{self.__class__.__name__}:{data.get('sensorId', 'UNK')}] Sent Data: {data}")
                self.total_sent += 1
                break  # Success
            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"[{self.__class__.__name__}] Attempt {attempt + 1}/{self.max_retries} failed: {e}"
                )
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.total_failed += 1
                    logger.error(f"[{self.__class__.__name__}] Ultimate failure sending data: {e}")

