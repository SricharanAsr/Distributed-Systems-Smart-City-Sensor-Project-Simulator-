# Contributing Guidelines

We welcome contributions to the Smart City Sensor Project! To maintain code quality and consistency, please follow these guidelines.

## Adding New Sensors

1.  **Inherit from `BaseSensor`**: All new sensors must inherit from the `BaseSensor` class in `simulator.py`.
2.  **Implement `generate_data`**: Override the `generate_data` method to return a dictionary with the sensor's specific data points.
3.  **Include Metadata**: Every data packet must include `sensorId`, `city`, `zone`, `timestamp`, and `type`.
4.  **Register Sensor**: Update the main execution block in `simulator.py` to instantiate and use your new sensor.

## Coding Standards

- **PEP 8**: Follow standard Python coding conventions.
- **Type Hints**: Use type hints for method signatures where possible.
- **Documentation**: Add docstrings to new classes and complex methods.
- **Testing**: Add corresponding test cases in `test_sensors.py`.

## Pull Request Process

1.  Create a new branch for your feature or bugfix.
2.  Ensure all tests pass by running `python test_sensors.py`.
3.  Update documentation if you've added new features or changed behaviors.
4.  Submit a PR with a clear description of the changes.
