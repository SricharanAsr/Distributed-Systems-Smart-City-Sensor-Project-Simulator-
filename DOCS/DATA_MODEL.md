# Sensor Data Model

This document describes the data structure of the various sensors simulated in the Smart City Project.

## Common Fields

All sensor payloads include these fields:

| Field | Type | Description |
| --- | --- | --- |
| `sensorId` | `string` | Unique identifier for the sensor. |
| `city` | `string` | The city name where the sensor is located. |
| `zone` | `string` | The city zone (e.g., North, South, Industrial). |
| `timestamp` | `string` | ISO 8601 formatted timestamp. |

## Sensor Specific Data

### Traffic Sensor
| Field | Type | Description |
| --- | --- | --- |
| `vehicle_count` | `integer` | Number of vehicles detected in the interval. |
| `average_speed` | `float` | Average speed of vehicles in km/h. |

### Air Quality Sensor
| Field | Type | Description |
| --- | --- | --- |
| `pm25` | `float` | Particulate matter 2.5 concentration. |
| `pm10` | `float` | Particulate matter 10 concentration. |
| `co2` | `float` | Carbon dioxide concentration in ppm. |

### Waste Sensor
| Field | Type | Description |
| --- | --- | --- |
| `fill_level` | `float` | Bin fill percentage (0-100). |
| `weight` | `float` | Bin contents weight in kg. |

### Streetlight Sensor
| Field | Type | Description|
| --- | --- | ---|
| `is_on` | `boolean` | Lighting status. |
| `brightness` | `integer` | Luminosity percentage (0-100).|
| `power_consumption` | `float` | Kilowatts consumed.|

... (More sensors to be documented)
