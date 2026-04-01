import pytest
from typing import Dict, Any

@pytest.fixture
def mock_config() -> Dict[str, Any]:
    return {
        "backend_url": "http://localhost:8080/insert",
        "city": "TestCity",
        "zones": ["TestZone1", "TestZone2"],
        "sensor_ids": ["T101", "T102"],
        "interval": 1
    }
