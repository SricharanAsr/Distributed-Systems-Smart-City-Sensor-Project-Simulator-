import requests
import random
import time
import json
from datetime import datetime
from abc import ABC, abstractmethod

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
            print(f"[{self.__class__.__name__}] Sent Data:", data)
            print(f"[{self.__class__.__name__}] Server Response:", response.text)
        except Exception as e:
            print(f"[{self.__class__.__name__}] Error sending data:", e)

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

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_config()
    sensors = [
        EnvironmentSensor(config),
        TrafficSensor(config),
        WasteSensor(config)
    ]

    print("Smart City Simulator Started...")
    while True:
        for sensor in sensors:
            sensor.send_data()
        
        time.sleep(config.get("interval", 5))