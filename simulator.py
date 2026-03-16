import argparse
import requests
import random
import time
import json
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
from sensors import EnvironmentSensor, TrafficSensor, WasteSensor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SmartCitySimulator')

# Load environment variables from .env file if it exists
load_dotenv()

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