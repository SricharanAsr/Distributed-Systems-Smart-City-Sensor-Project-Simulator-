import pytest
from unittest.mock import patch, MagicMock
from simulator import SimulatorManager, load_config, validate_config
from typing import Dict, Any

def test_load_config_invalid_interval() -> None:
    config = {
        "backend_url": "http://test",
        "city": "Test",
        "zones": ["Z1"],
        "sensor_ids": ["S1"],
        "interval": -1
    }
    with pytest.raises(ValueError, match="positive integer"):
        validate_config(config)

def test_simulator_manager_init(mock_config: Dict[str, Any]) -> None:
    manager = SimulatorManager(mock_config)
    
    assert manager.interval == mock_config["interval"]
    assert len(manager.sensors) > 0  # Should dynamically load all sensors
    assert not manager._running

@patch("simulator.time.sleep")
def test_simulator_stop(mock_sleep: MagicMock, mock_config: Dict[str, Any]) -> None:
    manager = SimulatorManager(mock_config)
    manager.stop()
    assert manager.cancel_token.is_cancelled()
