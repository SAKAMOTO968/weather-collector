from dataclasses import dataclass

@dataclass
class WeatherRecord:
    date: str
    temperature_max: float
    temperature_min: float
    precipitation: float
    windspeed_max: float