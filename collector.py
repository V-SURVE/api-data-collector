from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import pandas as pd
import requests
from sqlalchemy import create_engine

load_dotenv()

CITIES = [
    ("Mumbai", 19.0760, 72.8777),
    ("London", 51.5074, -0.1278),
    ("Tokyo", 35.6762, 139.6503),
]

def fetch_city_weather(city: str, lat: float, lon: float) -> dict | None:
      url = (
          "https://api.open-meteo.com/v1/forecast"
          f"?latitude={lat}&longitude={lon}&current_weather=true"
      )
      try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        current = response.json()["current_weather"]

        return {
            "city": city,
            "temperature_c": current["temperature"],
            "windspeed_kmh": current["windspeed"],
            "recorded_at": datetime.now(timezone.utc).replace(tzinfo=None),
        }
      except Exception as exc:
        print(f"Skipping {city} due to error: {exc}")
        return None



def main() -> None:
  db_url = os.getenv("DATABASE_URL")
  if not db_url:
    raise ValueError("DATABASE_URL is missing in your .env file.")

  rows = []
  for city, lat, lon in CITIES:
    record = fetch_city_weather(city, lat, lon)
    if record is not None:
      rows.append(record)

  if not rows:
    print("No records fetched; nothing written to PostgreSQL.")
    return

  df = pd.DataFrame(rows)
  engine = create_engine(db_url)

  df.to_sql("weather_readings", engine, if_exists="append", index=False)
  print(f"Inserted {len(df)} rows into weather_readings.")


if __name__ == "__main__":
  main()