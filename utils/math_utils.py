import random

def calculate_jitter(base_interval_sec: float, jitter_percentage: float = 0.1) -> float:
    """Calculates a randomized jitter applied to a base interval."""
    variation = base_interval_sec * jitter_percentage
    return base_interval_sec + random.uniform(-variation, variation)
