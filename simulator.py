import argparse
import time
import json
import logging
import os
import yaml
from dotenv import load_dotenv
from typing import List, Dict, Any
import inspect
import sensors
from concurrent.futures import ThreadPoolExecutor




import random
import signal
from utils.config_models import AppConfig
from utils.logging_utils import setup_logging
from sensors.constants import (
    DEFAULT_BACKEND_URL,
    JITTER_PERCENTAGE,
    MIN_SLEEP_TIME,
)

# Initial logger setup
logger = setup_logging()

# Load environment variables from .env file if it exists
load_dotenv()


class CancellationToken:
    """A light-weight token used to signal cancellation across threads.

    Attributes:
        _is_cancelled (bool): Internal state representing if cancellation was requested.
    """
    def __init__(self) -> None:
        self._is_cancelled: bool = False

    def cancel(self) -> None:
        """Triggers the cancellation signal."""
        self._is_cancelled = True

    def is_cancelled(self) -> bool:
        """Checks if cancellation has been requested.

        Returns:
            bool: True if cancelled, False otherwise.
        """
        return self._is_cancelled

def load_config(config_path: str = "config.json") -> AppConfig:
    """Loads configuration from a file and overrides with environment variables.

    Args:
        config_path: Path to the configuration file (JSON or YAML).

    Returns:
        AppConfig: A validated configuration model.
    """
    # Load defaults from config file
    raw_data = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                if config_path.endswith((".yaml", ".yml")):
                    raw_data = yaml.safe_load(f) or {}
                else:
                    raw_data = json.load(f)
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
        "DRY_RUN": "dry_run",
    }
    for env_key, config_key in env_mappings.items():
        val = os.getenv(env_key)
        if val:
            if config_key == "interval":
                try:
                    raw_data[config_key] = int(val)
                except ValueError:
                    logger.error(f"{env_key} must be an integer.")
            elif config_key == "dry_run":
                raw_data[config_key] = val.lower() == "true"
            else:
                raw_data[config_key] = val

    # Validate and return using Pydantic
    try:
        return AppConfig.model_validate(raw_data)
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        # Fallback to defaults if validation fails completely, or raise
        return AppConfig(backend_url=DEFAULT_BACKEND_URL)


class SimulatorManager:
    """Manages the lifecycle and orchestration of city sensor simulations.

    Initializes sensor objects based on available classes in the sensors module
    and manages their execution using a thread pool.

    Attributes:
        config (AppConfig): The validated simulation configuration.
        interval (int): Seconds between data transmissions.
        sensors (List[BaseSensor]): List of initialized sensor instances.
        cancel_token (CancellationToken): Token for synchronizing shutdown.
    """

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.interval = config.interval
        self.sensors = []
        for name, obj in inspect.getmembers(sensors):
            if inspect.isclass(obj) and issubclass(obj, sensors.BaseSensor) and obj is not sensors.BaseSensor:
                # BaseSensor expects Dict[str, Any], so we pass model_dump()
                self.sensors.append(obj(config.model_dump()))

        self._running = False
        self.cancel_token = CancellationToken()
        self.executor = ThreadPoolExecutor(max_workers=len(self.sensors) + 1)
        self.health_interval = 60

    def _run_sensor(self, sensor: Any) -> None:
        """Continuously runs a single sensor simulation loop.

        Args:
            sensor: The sensor instance to run.
        """
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
            
            # Improved fast-exit evaluation
            for _ in range(int(sleep_time)):
                if self.cancel_token.is_cancelled():
                    break
                time.sleep(1)
            # Sleep the fractional part
            remaining = sleep_time - int(sleep_time)
            if remaining > 0 and not self.cancel_token.is_cancelled():
                time.sleep(remaining)

    def _log_health(self) -> None:
        """Periodically calculates and logs overall simulation health statistics."""
        for _ in range(self.health_interval):
            if self.cancel_token.is_cancelled():
                return
            time.sleep(1)

        while not self.cancel_token.is_cancelled():
            total_sent = sum(getattr(s, 'total_sent', 0) for s in self.sensors)
            total_failed = sum(getattr(s, 'total_failed', 0) for s in self.sensors)
            total = total_sent + total_failed
            success_rate = (total_sent / total * 100) if total > 0 else 100.0

            logger.info("--- Simulation Health Report ---")
            logger.info(f"Sensors Active: {len(self.sensors)}")
            logger.info(f"Total Packets Sent: {total_sent}")
            logger.info(f"Total Packets Failed: {total_failed}")
            logger.info(f"Success Rate: {success_rate:.2f}%")
            logger.info("--------------------------------")

            for _ in range(self.health_interval):
                if self.cancel_token.is_cancelled():
                    break
                time.sleep(1)

    def start(self) -> None:
        """Initiates the simulation by launching sensor threads."""
        self._running = True
        logger.info(f"Smart City Simulator Started with {len(self.sensors)} sensors...")

        for sensor in self.sensors:
            self.executor.submit(self._run_sensor, sensor)

        # Start health logging thread
        self.executor.submit(self._log_health)

        # Keep the main thread alive
        while self._running:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break

    def stop(self) -> None:
        """Shuts down all threads and releases resources."""
        logger.info("Stopping Smart City Simulator...")
        self.cancel_token.cancel()
        self._running = False
        self.executor.shutdown(wait=True, cancel_futures=True)
        logger.info("Simulator gracefully stopped.")


def main():
    """Main entry point for the Smart City Sensor Simulator CLI."""
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

    # Signal handling for graceful shutdown
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}. Shutting down...")
        manager.stop()
        os._exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        manager.start()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        manager.stop()


def run_healthcheck(manager: SimulatorManager) -> None:
    """Performs a diagnostic check on simulator connectivity and configuration.

    Args:
        manager: The SimulatorManager instance to check.
    """
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

# Generator loop optimizations
