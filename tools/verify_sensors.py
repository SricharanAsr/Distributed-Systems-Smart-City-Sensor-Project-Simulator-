import inspect
import sys
import os
from typing import List, Type

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sensors
from sensors.base import BaseSensor


def verify_all_sensors():
    """
    Instantiates every sensor class found in the sensors module 
    and verifies that they can generate valid data payloads.
    """
    print("=== Sensor Verification Tool ===")
    
    # Mock configuration for initialization
    mock_config = {
        "backend_url": "http://localhost:8080",
        "city": "VerifyCity",
        "zones": ["VerifyZone"],
        "sensor_ids": ["V101"],
        "interval": 1
    }

    sensor_classes: List[Type[BaseSensor]] = []
    
    # Discovery
    for name, obj in inspect.getmembers(sensors):
        if (inspect.isclass(obj) and 
            issubclass(obj, BaseSensor) and 
            obj is not BaseSensor):
            sensor_classes.append(obj)

    print(f"Discovered {len(sensor_classes)} sensor implementations.")
    print("-" * 30)

    success_count = 0
    failure_count = 0

    for cls in sensor_classes:
        sensor_name = cls.__name__
        try:
            # Instantiate
            instance = cls(mock_config)
            
            # Generate sample data
            data = instance.generate_data()
            
            # Basic validation
            required_keys = ["sensorId", "city", "zone", "timestamp", "type"]
            missing = [k for k in required_keys if k not in data]
            
            if missing:
                print(f"[FAIL] {sensor_name}: Missing required keys {missing}")
                failure_count += 1
            else:
                print(f"[PASS] {sensor_name}: Generated payload for {data.get('type')}")
                success_count += 1
                
        except Exception as e:
            print(f"[ERROR] {sensor_name}: Initialization/Execution failed: {e}")
            failure_count += 1

    print("-" * 30)
    print(f"Results: {success_count} Passed, {failure_count} Failed.")
    
    if failure_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    verify_all_sensors()
