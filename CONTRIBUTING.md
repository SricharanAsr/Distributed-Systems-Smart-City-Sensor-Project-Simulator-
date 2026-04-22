# Contributing Guidelines

We welcome contributions! To maintain a high standard of quality, please follow these guidelines when contributing to the Smart City Sensor Simulator.

## Development Environment Setup

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/SricharanAsr/Distributed-Systems-Smart-City-Sensor-Project-Simulator-.git
    ```
2.  **Install Dependencies**:
    ```bash
    make install
    ```
3.  **Setup Linting/Formatting Tools**:
    We use `black`, `isort`, and `flake8`. You can run them via:
    ```bash
    make format
    make lint
    ```

## Adding New Sensors

1.  **Define the Data Model**:
    Add a new Pydantic model in `sensors/models.py`. Ensure it inherits from `BaseSensorData`.
2.  **Create the Sensor Class**:
    Create a new file in `sensors/` (e.g., `sensors/my_sensor.py`). Inherit from `BaseSensor`.
3.  **Implement `generate_data`**:
    Use your new model to return a structured payload.
4.  **Register the Sensor**:
    Add your sensor class to the `__init__.py` file in the `sensors/` directory. The `SimulatorManager` will automatically discover it.
5.  **Verify**:
    Run the verification tool to ensure your sensor works:
    ```bash
    make verify
    ```

## Testing Standards

- All new features should have corresponding tests in `tests/`.
- Run the full test suite before submitting:
  ```bash
  make test
  ```

## Pull Request Process

1.  Create a feature branch from `master`.
2.  Pass all linting and tests (`make lint test`).
3.  Submit your PR with a clear summary of changes and use cases.

### Running Tooling
Run `make verify` and `make export-test` natively.
