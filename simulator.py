import argparse
import time
import json
import logging
import os
import threading
from dotenv import load_dotenv
from typing import List, Dict, Any
from sensors import (
    EnvironmentSensor,
    TrafficSensor,
    WasteSensor,
    NoiseSensor,
    EnergySensor,
    WaterQualitySensor,
    AirQualitySensor,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("SmartCitySimulator")


class JsonFormatter(logging.Formatter):
    """
    Custom formatter to output logs in JSON format.
    """

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def setup_logging(json_format=False):
    handler = logging.StreamHandler()
    if json_format:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )

    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    # Prevent propagation to the root logger which has the default config
    logger.propagate = False

# Load environment variables from .env file if it exists
load_dotenv()


class CancellationToken:
    def __init__(self):
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def is_cancelled(self):
        return self._is_cancelled


def load_config(config_path="config.json"):
    # Load defaults from config.json
    config_data = {}
    try:
        with open(config_path, "r") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        logger.warning(
            f"{config_path} not found, relying on environment variables or defaults."
        )
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing {config_path}: {e}")

    # Override with environment variables
    env_mappings = {
        "BACKEND_URL": "backend_url",
        "CITY": "city",
        "SIMULATION_INTERVAL": "interval",
    }
    for env_key, config_key in env_mappings.items():
        val = os.getenv(env_key)
        if val:
            if config_key == "interval":
                try:
                    config_data[config_key] = int(val)
                except ValueError:
                    logger.error(f"{env_key} must be an integer.")
            else:
                config_data[config_key] = val

    # Apply fallbacks
    config_data.setdefault("backend_url", "http://localhost:8080/insert")
    config_data.setdefault("city", "UnknownCity")
    config_data.setdefault("zones", ["ZoneA"])
    config_data.setdefault("sensor_ids", ["S1"])
    config_data.setdefault("interval", 5)

    # Validation
    validate_config(config_data)

    return config_data


def validate_config(config: Dict[str, Any]) -> None:
    """Validates the configuration dictionary."""
    required_keys = ["backend_url", "city", "zones", "sensor_ids", "interval"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")

    if not isinstance(config["interval"], int) or config["interval"] <= 0:
        raise ValueError("Simulation interval must be a positive integer.")

    if not config["zones"] or not isinstance(config["zones"], list):
        raise ValueError("Zones must be a non-empty list.")

    if not config["sensor_ids"] or not isinstance(config["sensor_ids"], list):
        raise ValueError("Sensor IDs must be a non-empty list.")


class SimulatorManager:
    """
    Manages the initialization and continuous data transmission of smart city sensors.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.interval = config.get("interval", 5)
        self.sensors = [
            EnvironmentSensor(config),
            TrafficSensor(config),
            WasteSensor(config),
            NoiseSensor(config),
            EnergySensor(config),
            WaterQualitySensor(config),
            AirQualitySensor(config),
        ]
        self._running = False
        self.cancel_token = CancellationToken()
        self.threads: List[threading.Thread] = []

    def _run_sensor(self, sensor: Any) -> None:
        """Continuously runs a single sensor."""
        while not self.cancel_token.is_cancelled():
            sensor.send_data()
            for _ in range(self.interval):
                if self.cancel_token.is_cancelled():
                    break
                time.sleep(1)

    def start(self) -> None:
        """Starts the main simulation loop with multi-threading."""
        self._running = True
        logger.info(f"Smart City Simulator Started with {len(self.sensors)} sensors...")

        for sensor in self.sensors:
            thread = threading.Thread(target=self._run_sensor, args=(sensor,))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()

        # Keep the main thread alive
        while self._running:
            time.sleep(1)

    def stop(self) -> None:
        """Stops the simulation loop and joins threads."""
        logger.info("Stopping Smart City Simulator...")
        self.cancel_token.cancel()
        for thread in self.threads:
            thread.join(timeout=2)
        logger.info("Simulator gracefully stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart City Sensor Simulator")
    parser.add_argument(
        "--config", type=str, default="config.json", help="Path to configuration file"
    )
    parser.add_argument(
        "--health", action="store_true", help="Run a health check and exit"
    )
    args = parser.parse_args()

    config = load_config(args.config)

    # Use JSON logging if configured or via env var
    use_json = config.get("json_logging", os.getenv("JSON_LOGGING", "false").lower() == "true")
    setup_logging(json_format=use_json)

    manager = SimulatorManager(config)
    try:
        manager.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Shutting down...")
        manager.stop()


def run_healthcheck(manager: SimulatorManager) -> None:
    """Performs a health check on the simulator components."""
    logger.info("Starting Simulator Health Check...")
    errors = []

    # Check backend connectivity (optional/soft check)
    try:
        import requests
        resp = requests.get(manager.config["backend_url"].replace("/insert", ""), timeout=2)
        logger.info(f"Backend connectivity check (GET): {'Success' if resp.status_code < 500 else 'Failed'}")
    except Exception as e:
        logger.warning(f"Backend connectivity check failed (non-critical): {e}")

    # Check if sensors are initialized
    if not manager.sensors:
        errors.append("No sensors initialized.")
    else:
        logger.info(f"Initialized {len(manager.sensors)} sensors.")

    # Validate interval
    if manager.interval <= 0:
        errors.append(f"Invalid interval: {manager.interval}")

    if errors:
        logger.error("Health Check FAILED:")
        for err in errors:
            logger.error(f" - {err}")
        exit(1)
    else:
        logger.info("Health Check PASSED.")
        exit(0)
