class SmartCityException(Exception):
    pass

class SensorNotConfiguredError(SmartCityException):
    pass

class SensorDataInvalidError(SmartCityException):
    pass

# Utilizing domain specific exceptions optimizes upper level Simulator rescue operations.
