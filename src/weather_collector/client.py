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
    
def fetch_history(
    latitude: float, longitude: float, start_date: str, end_date: str
) -> list[WeatherRecord]:
    """
    Fetch historical weather data from Open-Meteo Archive API.
    
    Args:
        latitude: เส้นรุ้ง
        longitude: เส้นแวง
        start_date: วันที่เริ่มต้น format "YYYY-MM-DD"
        end_date: วันสิ้นสุด format "YYYY-MM-DD"
        
    Returns:
        list of WeatherRecord
        
    Raises:
        WeatherAPIError: ถ้า API ตอบกลับผิดพลาด
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
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
    
    return _parse_response(response.json())