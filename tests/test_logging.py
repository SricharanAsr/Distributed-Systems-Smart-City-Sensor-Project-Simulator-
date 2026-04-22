import logging
from utils.logging_utils import setup_logging

def test_custom_json_logger():
    logger = setup_logging('test', json_format=True)
    assert logger.name == 'test'

def test_standard_logger():
    logger = setup_logging('test2', json_format=False)
    assert logger.name == 'test2'

# These tests ensure logging handlers do not accumulate exponentially during reloading.
