import pytest
from unittest.mock import patch, MagicMock
from sensors.base import BaseSensor
from typing import Dict, Any

class DummySensor(BaseSensor):
    def generate_data(self) -> Dict[str, Any]:
        return {"test": "data", "sensorId": self.sensor_ids[0]}

def test_base_sensor_initialization(mock_config: Dict[str, Any]) -> None:
    sensor = DummySensor(mock_config)
    assert sensor.backend_url == mock_config["backend_url"]
    assert sensor.city == mock_config["city"]
    assert sensor.zones == mock_config["zones"]
    assert sensor.sensor_ids == mock_config["sensor_ids"]

@patch("sensors.base.requests.post")
def test_send_data_success(mock_post: MagicMock, mock_config: Dict[str, Any]) -> None:
    mock_post.return_value.status_code = 200
    mock_post.return_value.raise_for_status = MagicMock()
    
    sensor = DummySensor(mock_config)
    sensor.send_data()
    
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["json"] == {"test": "data", "sensorId": "T101"}
