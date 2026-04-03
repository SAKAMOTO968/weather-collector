import httpx
from .models import WeatherRecord

class WeatherAPIError(Exception):
    pass

def fetch_weather(latitude: float, longitude: float, days: int = 7) -> list[WeatherRecord]:
    """
    Fetch weather forecast from Open_Meteo API
    
    Args:
        latitude: เส้นรุ้ง เช่น 13.75 สำหรับกรุงเทพ
        longitude: เส้นแวง เช่น 100.52 สำหรับกรุงเทพ
        days: จำนวนวันที่ต้องการ

    Returns:
        list of WeatherRecord
        
    Raises:
        WeatherAPIError: ถ้า API ตอบกลับผิดพลาด
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "timezone": "auto",
        "forecast_days": days,
        "timezone": "Asia/Bangkok",
    }
    
    try:
        response = httpx.get(url, params=params, timeout=10.0)
        response.raise_for_status()
    except httpx.TimeoutException:
        raise WeatherAPIError("Request timed out")
    except httpx.HTTPStatusError as e:
        raise WeatherAPIError(f"API returned {e.response.status_code}")
    except httpx.RequestError as e:
        raise WeatherAPIError(f"Connection error: {e}")
    
    data = response.json() 
    return _parse_response(data)

def _parse_response(data: dict) -> list[WeatherRecord]:
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    temp_max = daily.get("temperature_2m_max", [])
    temp_min = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    wind = daily.get("windspeed_10m_max", [])
    
    return [
        WeatherRecord(
            date=dates[i],
            temperature_max=temp_max[i] or 0.0,
            temperature_min=temp_min[i] or 0.0,
            precipitation=precip[i] or 0.0,
            windspeed_max=wind[i] or 0.0
        )
        for i in range(len(dates))
    ]