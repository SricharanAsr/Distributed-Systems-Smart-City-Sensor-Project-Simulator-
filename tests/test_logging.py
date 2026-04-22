import logging
from utils.logging_utils import setup_logging

def test_custom_json_logger():
    logger = setup_logging('test', json_format=True)
    assert logger.name == 'test'
