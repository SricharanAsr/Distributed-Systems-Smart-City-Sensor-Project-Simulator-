# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite setup with `pytest`
- `ParkingSensor` and `StreetLightSensor` to expand data points
- Explicit HTTP retry logic with exponential backoff for resilience
- `config.yaml` support for flexible environment configuration
- Centralized JSON-compatible logging via `utils/logging_utils.py`
- Architectural documentation and API specification examples
- Periodic health status reporting for long-running simulators
- "Dry run" mode to allow local testing without API connectivity
- `pyproject.toml` configuration for standard build tools

### Changed
- Standardized sensor initialization dynamically using `inspect`
- Optimized `requests.Session` per sensor to minimize connection overhead
- General modernization of the class structure with `pydantic` v2

## [1.0.0] - Initial Release
- Basic Smart City Simulator skeleton
- Environment, Traffic, Waste, Noise, Energy, Water Quality, and Air Quality sensors
