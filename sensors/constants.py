# Simulation Constants

DEFAULT_BACKEND_URL = "http://localhost:8080/insert"
DEFAULT_CITY = "UnknownCity"
DEFAULT_ZONES = ["ZoneA"]
DEFAULT_SENSOR_IDS = ["S1"]
DEFAULT_INTERVAL = 5

# Sensor Type Names
TYPE_ENVIRONMENT = "environment"
TYPE_TRAFFIC = "traffic"
TYPE_WASTE = "waste"
TYPE_NOISE = "noise"
TYPE_ENERGY = "energy"
TYPE_WATER_QUALITY = "water_quality"
TYPE_AIR_QUALITY = "air_quality"
TYPE_PARKING = "parking"
TYPE_STREETLIGHT = "streetlight"
TYPE_HUMIDITY = "humidity"
TYPE_PRESSURE = "pressure"

# Traffic Range Constants
TRAFFIC_COUNT_MIN = 0
TRAFFIC_COUNT_MAX = 100
TRAFFIC_SPEED_MIN = 10.0
TRAFFIC_SPEED_MAX = 80.0

# Environment/Humidity Range Constants
TEMP_MIN = -50.0
TEMP_MAX = 60.0
HUMIDITY_MIN = 0.0
HUMIDITY_MAX = 100.0

# Air Quality Ranges
PM25_MAX = 500.0
CO2_MAX = 2000.0

# Simulation Parameters
JITTER_PERCENTAGE = 0.2
MIN_SLEEP_TIME = 1
GRACEFUL_SHUTDOWN_TIMEOUT = 2
DEFAULT_JSON_LOGGING = False
HTTP_TIMEOUT = 10
