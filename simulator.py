import argparse
import requests
import random
import time
import json
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
from abc import ABC, abstractmethod

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SmartCitySimulator')

# Load environment variables from .env file if it exists
load_dotenv()

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

class EnvironmentSensor(BaseSensor):
    """
    Simulates environmental factors such as temperature, humidity, and air quality.
    """
    def generate_data(self):
        return {
            "sensorId": random.choice(self.sensor_ids),
            "city": self.city,
            "zone": random.choice(self.zones),
            "temperature": round(random.uniform(25, 40), 2),
            "humidity": random.randint(40, 80),
            "aqi": random.randint(50, 300),
            "co2": random.randint(350, 500),
            "timestamp": datetime.now().isoformat(),
            "type": "environment"
        }

class TrafficSensor(BaseSensor):
    """
    Simulates traffic flow data including vehicle counts and average speeds.
    """
    def generate_data(self):
        return {
            "sensorId": random.choice(self.sensor_ids),
            "city": self.city,
            "zone": random.choice(self.zones),
            "vehicle_count": random.randint(0, 100),
            "average_speed": round(random.uniform(10, 60), 2),
            "timestamp": datetime.now().isoformat(),
            "type": "traffic"
        }

class WasteSensor(BaseSensor):
    """
    Simulates waste management metrics such as bin fill levels.
    """
    def generate_data(self):
        return {
            "sensorId": random.choice(self.sensor_ids),
            "city": self.city,
            "zone": random.choice(self.zones),
            "fill_level": random.randint(0, 100),
            "last_collected": datetime.now().isoformat(),
            "timestamp": datetime.now().isoformat(),
            "type": "waste"
        }

def load_config(config_path="config.json"):
    # Load defaults from config.json
    config_data = {}
    try:
        with open(config_path, "r") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        logger.warning("config.json not found, relying solely on environment variables or defaults.")
    
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart City Sensor Simulator")
    parser.add_argument('--config', type=str, default="config.json", help="Path to configuration file")
    args = parser.parse_args()

    config = load_config(args.config)
    sensors = [
        EnvironmentSensor(config),
        TrafficSensor(config),
        WasteSensor(config)
    ]

    logger.info("Smart City Simulator Started...")
    while True:
        for sensor in sensors:
            sensor.send_data()
        
        time.sleep(config.get("interval", 5))