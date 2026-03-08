# Development Guide

This document provides more detailed information for developers who want to set up and modify the Smart City Simulator.

## Local Environment Setup

### Prerequisites
- Python 3.8 or higher.
- `pip` for package management.

### Installation Steps
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/SricharanAsr/Distributed-Systems-Smart-City-Sensor-Project-Simulator-.git
    cd Distributed-Systems-Smart-City-Sensor-Project-Simulator-
    ```
2.  **Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Unix/macOS:
    source venv/bin/activate
    ```
3.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```

## Running & Debugging

### Running the Simulator
Standard execution:
```bash
python simulator.py
```

### Running Tests
We use the `unittest` framework:
```bash
python test_sensors.py
```

### Debugging Tips
- Check the console output for `[SensorName] Sent Data` messages.
- If the server response is an error, verify the `backend_url` in `config.json`.
- Ensure your machine has network access to the target IP address.

## Project Structure
- `simulator.py`: Core logic and sensor class definitions.
- `config.json`: Environment-specific configuration.
- `test_sensors.py`: Unit tests.
- `README.md`: High-level overview.
