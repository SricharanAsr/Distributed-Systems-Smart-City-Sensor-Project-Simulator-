import argparse
import time
import json
import logging
import os
import threading
import yaml
from dotenv import load_dotenv
from typing import List, Dict, Any
import inspect
import sensors



from utils.logging_utils import setup_logging
from sensors.constants import (
    DEFAULT_BACKEND_URL,
    DEFAULT_CITY,
    DEFAULT_ZONES,
    DEFAULT_SENSOR_IDS,
    DEFAULT_INTERVAL,
    JITTER_PERCENTAGE,
    MIN_SLEEP_TIME,
    GRACEFUL_SHUTDOWN_TIMEOUT,
)

# Initial logger setup
logger = setup_logging()

# Load environment variables from .env file if it exists
load_dotenv()


class CancellationToken:
    def __init__(self) -> None:
        self._is_cancelled: bool = False

    def cancel(self) -> None:
        self._is_cancelled = True

    def is_cancelled(self) -> bool:
        return self._is_cancelled



def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    # Load defaults from config file
    config_data = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                if config_path.endswith((".yaml", ".yml")):
                    config_data = yaml.safe_load(f) or {}
                else:
                    config_data = json.load(f)
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            logger.error(f"Error parsing {config_path}: {e}")
    else:
        logger.warning(
            f"Config file '{config_path}' not found, relying on environment variables or defaults."
        )
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
    config_data.setdefault("backend_url", DEFAULT_BACKEND_URL)
    config_data.setdefault("city", DEFAULT_CITY)
    config_data.setdefault("zones", DEFAULT_ZONES)
    config_data.setdefault("sensor_ids", DEFAULT_SENSOR_IDS)
    config_data.setdefault("interval", DEFAULT_INTERVAL)

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
        self.sensors = []
        for name, obj in inspect.getmembers(sensors):
            if inspect.isclass(obj) and issubclass(obj, sensors.BaseSensor) and obj is not sensors.BaseSensor:
                self.sensors.append(obj(config))



        self._running = False
        self.cancel_token = CancellationToken()
        self.threads: List[threading.Thread] = []

    def _run_sensor(self, sensor: Any) -> None:
        """Continuously runs a single sensor with randomized jitter."""
        # Initial random delay to desynchronize sensors
        initial_delay = random.uniform(0, self.interval)
        for _ in range(int(initial_delay)):
            if self.cancel_token.is_cancelled():
                return
            time.sleep(1)

        while not self.cancel_token.is_cancelled():
            sensor.send_data()
            # Add jitter
            jitter = random.uniform(-JITTER_PERCENTAGE * self.interval, JITTER_PERCENTAGE * self.interval)
            sleep_time = max(MIN_SLEEP_TIME, self.interval + jitter)
            
            for _ in range(int(sleep_time)):
                if self.cancel_token.is_cancelled():
                    break
                time.sleep(1)
            # Sleep the fractional part
            remaining = sleep_time - int(sleep_time)
            if remaining > 0 and not self.cancel_token.is_cancelled():
                time.sleep(remaining)

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
            thread.join(timeout=GRACEFUL_SHUTDOWN_TIMEOUT)
        logger.info("Simulator gracefully stopped.")


def main():
    parser = argparse.ArgumentParser(description="Smart City Sensor Simulator")
    parser.add_argument(
        "--config", type=str, default="config.json", help="Path to configuration file"
    )
    parser.add_argument(
        "--health", action="store_true", help="Run a health check and exit"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Run simulation without sending API calls"
    )
    args = parser.parse_args()

    config = load_config(args.config)
    config["dry_run"] = args.dry_run


    # Use JSON logging if configured or via env var
    use_json = config.get("json_logging", os.getenv("JSON_LOGGING", "false").lower() == "true")
    setup_logging(json_format=use_json)

    manager = SimulatorManager(config)

    if args.health:
        run_healthcheck(manager)
        return

    try:
        manager.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Shutting down...")
        manager.stop()


if __name__ == "__main__":
    main()


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
