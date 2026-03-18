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
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("SmartCitySimulator")

# Load environment variables from .env file if it exists
load_dotenv()


def load_config(config_path="config.json"):
    # Load defaults from config.json
    config_data = {}
    try:
        with open(config_path, "r") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        logger.warning(
            "config.json not found, relying solely on environment variables or defaults."
        )

    # Override with environment variables
    if os.getenv("BACKEND_URL"):
        config_data["backend_url"] = os.getenv("BACKEND_URL")
    if os.getenv("CITY"):
        config_data["city"] = os.getenv("CITY")
    if os.getenv("SIMULATION_INTERVAL"):
        try:
            config_data["interval"] = int(os.getenv("SIMULATION_INTERVAL"))
        except ValueError:
            logger.error("SIMULATION_INTERVAL must be an integer.")

    # Apply fallbacks if not set
    config_data.setdefault("backend_url", "http://localhost:8080/insert")
    config_data.setdefault("city", "UnknownCity")
    config_data.setdefault("zones", ["ZoneA"])
    config_data.setdefault("sensor_ids", ["S1"])
    config_data.setdefault("interval", 5)

    return config_data


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
        ]
        self._running = False
        self.threads: List[threading.Thread] = []

    def _run_sensor(self, sensor: Any) -> None:
        """Continuously runs a single sensor."""
        while self._running:
            sensor.send_data()
            time.sleep(self.interval)

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
        self._running = False
        logger.info("Stopping Smart City Simulator...")
        for thread in self.threads:
            thread.join(timeout=2)
        logger.info("Simulator gracefully stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart City Sensor Simulator")
    parser.add_argument(
        "--config", type=str, default="config.json", help="Path to configuration file"
    )
    args = parser.parse_args()

    config = load_config(args.config)

    manager = SimulatorManager(config)
    try:
        manager.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Shutting down...")
        manager.stop()
