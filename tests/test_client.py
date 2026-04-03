import pytest
import respx
import httpx
from weather_collector.client import fetch_weather, WeatherAPIError

MOCK_RESPONSE = {
    "daily": {
        "time": ["2024-04-03", "2024-04-04", "2024-04-05"],
        "temperature_2m_max": [34.3, 34.0, 35.1],
        "temperature_2m_min": [27.5, 27.4, 27.7],
        "precipitation_sum": [0.0, 0.0, 1.2],
        "windspeed_10m_max": [12.5, 13.1, 11.6]
    }
}

@respx.mock
def test_fetch_weather_returns_correct_records():
    respx.get("https://api.open-meteo.com/v1/forecast").mock(
        return_value=httpx.Response(200, json=MOCK_RESPONSE)
    )
    
    records = fetch_weather(13.75, 100.52, days=3)
    
    assert len(records) == 3
    assert records[0].date == "2024-04-03"
    assert records[0].temperature_max == 34.3
    assert records[2].precipitation == 1.2
 

@respx.mock
def test_fetch_weather_handles_timeout():
    respx.get("https://api.open-meteo.com/v1/forecast").mock(
        side_effect=httpx.TimeoutException("timedout")
    )
    with pytest.raises(WeatherAPIError, match="timed out"):
        fetch_weather(13.75, 100.52)
    
@respx.mock
def test_fetch_weather_handles_server_error():
    respx.get("https://api.open-meteo.com/v1/forecast").mock(
        return_value=httpx.Response(500)
    )
    with pytest.raises(WeatherAPIError, match="500"):
        fetch_weather(13.75, 100.52)