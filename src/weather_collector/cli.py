import argparse
from .client import fetch_weather, WeatherAPIError
from .storage import save_csv

CITIES = {
    "bangkok": (13.75, 100.52),
    "chiangmai": (18.79, 98.98),
    "phuket": (7.89, 98.40),
}

def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch weather data")
    parser.add_argument(
        "city",
        choices=list(CITIES.keys()),
        help="City to fetch weather for"
    )
    parser.add_argument(
        "--days", type=int, default=7, help="Number of forecast days (default: 7)",
    )
    parser.add_argument(
        "--output", default="weather.csv", help="Output CSV file (default: weather.csv)",
    )
    args = parser.parse_args()
    
    lat, lon = CITIES[args.city]
    print(f"Fetching {args.days}-day forecast for {args.city}...")
    
    try:
        records = fetch_weather(lat, lon, days=args.days)
        save_csv(records, args.output)
    except WeatherAPIError as e:
        print(f"Error {e}")
        return
    
    print(f"\nPreview")
    for r in records[:3]:
        print(f" {r.date} max:{r.temperature_max}°C min:{r.temperature_min}°C rain:{r.precipitation}mm")
        
if __name__ == "__main__":
    main()