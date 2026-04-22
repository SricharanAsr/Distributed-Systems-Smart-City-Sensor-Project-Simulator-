import pytest
import time
from unittest.mock import patch, MagicMock
from sensors.base import BaseSensor
from typing import Dict, Any
import requests

class DummySensor(BaseSensor):
    def generate_data(self) -> Dict[str, Any]:
        return {"test": "data", "sensorId": self.sensor_ids[0]}

def test_base_sensor_initialization(mock_config: Dict[str, Any]) -> None:
    sensor = DummySensor(mock_config)
    assert sensor.backend_url == mock_config["backend_url"]
    assert sensor.city == mock_config["city"]
    assert sensor.zones == mock_config["zones"]
    assert sensor.sensor_ids == mock_config["sensor_ids"]

@patch("sensors.base.requests.Session.post")
def test_send_data_success(mock_post: MagicMock, mock_config: Dict[str, Any]) -> None:
    mock_post.return_value.status_code = 200
    mock_post.return_value.raise_for_status = MagicMock()
    
    sensor = DummySensor(mock_config)
    sensor.send_data()
    
    mock_post.assert_called_once()
    _, kwargs = mock_post.call_args
    assert kwargs["json"] == {"test": "data", "sensorId": "T101"}
    assert sensor.total_sent == 1

@patch("sensors.base.time.sleep", return_value=None)
@patch("sensors.base.requests.Session.post")
def test_send_data_retry_success(mock_post: MagicMock, mock_sleep: MagicMock, mock_config: Dict[str, Any]) -> None:
    # Fail first, then succeed
    fail_resp = MagicMock()
    fail_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("Failure")
    
    success_resp = MagicMock()
    success_resp.status_code = 200
    
    mock_post.side_effect = [fail_resp, success_resp]
    
    sensor = DummySensor(mock_config)
    sensor.send_data()
    
    assert mock_post.call_count == 2
    assert sensor.total_sent == 1
    mock_sleep.assert_called_once_with(1) # first retry wait time is 2^0 = 1

@patch("sensors.base.time.sleep", return_value=None)
@patch("sensors.base.requests.Session.post")
def test_send_data_ultimate_failure(mock_post: MagicMock, mock_sleep: MagicMock, mock_config: Dict[str, Any]) -> None:
    mock_post.side_effect = requests.exceptions.RequestException("Fatal")
    
    sensor = DummySensor(mock_config)
    sensor.send_data()
    
    assert mock_post.call_count == 3 # Default max_retries
    assert sensor.total_failed == 1
    assert sensor.total_sent == 0

def test_dry_run_logic(mock_config: Dict[str, Any]) -> None:
    mock_config["dry_run"] = True
    sensor = DummySensor(mock_config)
    
    with patch("sensors.base.requests.Session.post") as mock_post:
        sensor.send_data()
        mock_post.assert_not_called()
        assert sensor.total_sent == 0
