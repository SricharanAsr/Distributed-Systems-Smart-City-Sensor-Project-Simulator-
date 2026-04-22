import random
import json
import os
import requests
import logging
import time
from typing import Dict, Any, List, Optional, Protocol, runtime_checkable
from abc import ABC, abstractmethod

logger = logging.getLogger("SmartCitySimulator")

@runtime_checkable
class Sensor(Protocol):
    """Protocol for sensor types for static type checking."""
    def send_data(self) -> None: ...
    def generate_data(self) -> Dict[str, Any]: ...

class BaseSensor(ABC):
    """
    Abstract base class for all smart city sensors.
    Provides logic for HTTP session management, data transmission with retry,
    and probabilistic failure injection.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config: Dict[str, Any] = config
        self.backend_url: str = config.get("backend_url", "")
        self.city: str = config.get("city", "")
        self.zones: List[str] = config.get("zones", [])
        self.sensor_ids: List[str] = config.get("sensor_ids", [])
        self.dry_run: bool = config.get("dry_run", False)
        self.max_retries: int = config.get("max_retries", 3)
        self.cache_dir: str = config.get("cache_dir", "data_cache")
        
        # Reliability Parameters
        self.failure_probability: float = config.get("failure_probability", 0.0)
        self.jitter_multiplier: float = config.get("jitter_multiplier", 1.0)
        
        # Statistics tracking
        self.total_sent: int = 0
        self.total_failed: int = 0
        
        # Persistent HTTP session for connection pooling
        self.session: requests.Session = requests.Session()
        
    def __del__(self) -> None:
        """Ensure cleanup of resources on deletion."""
        self.close()

    def close(self) -> None:
        """Closes the underlying HTTP session."""
        if hasattr(self, 'session'):
            self.session.close()

    @abstractmethod
    def generate_data(self) -> Dict[str, Any]:
        """must be implemented by subclasses to return sensor-specific payload."""
        pass

    def _execute_request_with_retry(self, data: Dict[str, Any]) -> requests.Response:
        """Sends POST request to backend with a configured timeout."""
        return self.session.post(self.backend_url, json=data, timeout=10)

    def _cache_failed_data(self, data: Dict[str, Any]) -> None:
        """Saves failed payload to local storage for offline auditing."""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        filename = f"{self.__class__.__name__}_{int(time.time() * 1000)}.json"
        filepath = os.path.join(self.cache_dir, filename)
        
        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            logger.info(f"[{self.__class__.__name__}] Cached failed payload to {filepath}")
        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] Failed to cache data locally: {e}")

    def send_data(self) -> None:
        """Simulates reading sensor data and transmitting it to the backend."""
        # Random Failure Injection (Malfunction simulation)
        if random.random() < self.failure_probability:
            logger.warning(f"[{self.__class__.__name__}] Simulated internal hardware failure. Skipping packet.")
            self.total_failed += 1
            return

        data = self.generate_data()
        
        if self.dry_run:
            logger.info(f"[DRY-RUN] {self.__class__.__name__} payload: {data}")
            return
        
        for attempt in range(self.max_retries):
            try:
                response = self._execute_request_with_retry(data)
                response.raise_for_status()

                logger.debug(f"[{self.__class__.__name__}:{data.get('sensorId', 'UNK')}] Successfully sent data.")
                self.total_sent += 1
                return  # Success exit
            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"[{self.__class__.__name__}] Transmission attempt {attempt + 1}/{self.max_retries} failed: {e}"
                )
                if attempt < self.max_retries - 1:
                    # Apply jitter to backoff
                    wait_time = (2 ** attempt) * random.uniform(0.5, 1.5) * self.jitter_multiplier
                    logger.debug(f"Retrying in {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                else:
                    self.total_failed += 1
                    logger.error(f"[{self.__class__.__name__}] Failed to send data after {self.max_retries} attempts.")
                    self._cache_failed_data(data)

