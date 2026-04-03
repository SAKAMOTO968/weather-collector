import argparse
from .client import fetch_weather, fetch_history, WeatherAPIError
from .storage import save_csv

CITIES = {
    "bangkok":   (13.75, 100.52),
    "chiangmai": (18.79, 98.98),
    "phuket":    (7.89, 98.40),
}

def main():
    parser = argparse.ArgumentParser(description="Fetch weather data")
    parser.add_argument("city", choices=list(CITIES.keys()))
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--output", default="weather.csv")
    parser.add_argument("--history", action="store_true", help="Fetch historical data instead of forecast")
    parser.add_argument("--start", metavar="YYYY-MM-DD", help="Start date for history (required with --history)")
    parser.add_argument("--end", metavar="YYYY-MM-DD", help="End date for history (required with --history)")
    
    args = parser.parse_args()
    
    lat, lon = CITIES[args.city]
    
    if args.history:
        if not args.start or not args.end:
            print("Error: --history requires --start and --end dates")
            print("Example: weather bangkok --history --start 2026-01-01 --end 2026-01-31")
            return
        print(f"Fetching history for {args.city} from {args.start} to {args.end}...")
        try:
            records = fetch_history(lat, lon, args.start, args.end)
        except WeatherAPIError as e:
            print(f"Error: {e}")
            return
    else:
        print(f"Fetching {args.days}-day forecast for {args.city}...")
        try:
            records = fetch_weather(lat, lon, days=args.days)
        except WeatherAPIError as e:
            print(f"Error: {e}")
            return
       
    save_csv(records, args.output)
    print(f"\nPreview:")
    for r in records[:3]:
        print(f" {r.date} max:{r.temperature_max}°C min:{r.temperature_min}°C rain:{r.precipitation}mm")    

if __name__ == "__main__":
    main() 