import unittest
from sensors import EnvironmentSensor, TrafficSensor, WasteSensor, NoiseSensor

class TestSensors(unittest.TestCase):
    def setUp(self):
        self.config = {
            "backend_url": "http://localhost:8080/insert",
            "city": "TestCity",
            "zones": ["ZoneA"],
            "sensor_ids": ["S001"],
            "interval": 1
        }

    def test_environment_sensor_data(self):
        sensor = EnvironmentSensor(self.config)
        data = sensor.generate_data()
        self.assertEqual(data["city"], "TestCity")
        self.assertEqual(data["type"], "environment")
        self.assertIn("temperature", data)

    def test_traffic_sensor_data(self):
        sensor = TrafficSensor(self.config)
        data = sensor.generate_data()
        self.assertEqual(data["type"], "traffic")
        self.assertIn("vehicle_count", data)

    def test_waste_sensor_data(self):
        sensor = WasteSensor(self.config)
        data = sensor.generate_data()
        self.assertEqual(data["type"], "waste")
        self.assertIn("fill_level", data)

    def test_noise_sensor_data(self):
        sensor = NoiseSensor(self.config)
        data = sensor.generate_data()
        self.assertEqual(data["type"], "noise")
        self.assertIn("decibels", data)

if __name__ == "__main__":
    unittest.main()
