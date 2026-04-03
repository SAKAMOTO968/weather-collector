import csv
from pathlib import Path
from .models import WeatherRecord

def save_csv(records: list[WeatherRecord], output_path: str | Path) -> None:
    """Save weather records to CSV file"""
    path = Path(output_path)
    fieldnames = ["date", "temperature_max", "temperature_min", "precipitation", "windspeed_max"]
    
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({
                "date": record.date,
                "temperature_max": record.temperature_max,
                "temperature_min": record.temperature_min,
                "precipitation": record.precipitation,
                "windspeed_max": record.windspeed_max
            })
            
    print(f"Saved {len(records)} records to {path}")