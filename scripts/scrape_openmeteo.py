# ============================================================
# AirSense PK — Script 1b: Weather Data Fetcher
# Fetches weather variables separately since archive API
# does not accept future dates
# ============================================================

import requests
import pandas as pd
import os
import time

CITIES = [
    {"name": "Lahore",      "lat": 31.5497, "lon": 74.3436, "province": "Punjab"},
    {"name": "Faisalabad",  "lat": 31.4504, "lon": 73.1350, "province": "Punjab"},
    {"name": "Rawalpindi",  "lat": 33.6007, "lon": 73.0679, "province": "Punjab"},
    {"name": "Multan",      "lat": 30.1575, "lon": 71.5249, "province": "Punjab"},
    {"name": "Gujranwala",  "lat": 32.1877, "lon": 74.1945, "province": "Punjab"},
    {"name": "Karachi",     "lat": 24.8607, "lon": 67.0011, "province": "Sindh"},
    {"name": "Hyderabad",   "lat": 25.3960, "lon": 68.3578, "province": "Sindh"},
    {"name": "Islamabad",   "lat": 33.6844, "lon": 73.0479, "province": "ICT"},
    {"name": "Peshawar",    "lat": 34.0151, "lon": 71.5249, "province": "KPK"},
    {"name": "Quetta",      "lat": 30.1798, "lon": 66.9750, "province": "Balochistan"},
]

# Archive API only accepts dates up to a few days ago
# Using 2026-11-09 as safe cutoff (5 days before today)
START_DATE = "2022-01-01"
END_DATE   = "2026-11-09"

WEATHER_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
    "wind_direction_10m",
    "surface_pressure",
]

RAW_FOLDER = os.path.join("data", "raw")
os.makedirs(RAW_FOLDER, exist_ok=True)

print("=" * 50)
print("AirSense PK - Weather Fetcher")
print(f"Date range: {START_DATE} to {END_DATE}")
print("=" * 50)

all_dfs = []
failed  = []

for i, city in enumerate(CITIES, 1):
    name = city["name"]
    print(f"\n[{i}/10] Fetching weather for {name}...")

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude":   city["lat"],
        "longitude":  city["lon"],
        "hourly":     ",".join(WEATHER_VARS),
        "start_date": START_DATE,
        "end_date":   END_DATE,
        "timezone":   "Asia/Karachi",
    }

    try:
        r = requests.get(url, params=params, timeout=120)
        print(f"  Status: {r.status_code}")

        if r.status_code == 200:
            df = pd.DataFrame(r.json()["hourly"])
            df["city"]     = name
            df["province"] = city["province"]
            df["latitude"] = city["lat"]
            df["longitude"]= city["lon"]

            df = df.rename(columns={
                "time":                  "timestamp",
                "temperature_2m":        "temperature",
                "relative_humidity_2m":  "humidity",
                "wind_speed_10m":        "wind_speed",
                "wind_direction_10m":    "wind_direction",
                "surface_pressure":      "pressure",
            })

            filepath = os.path.join(RAW_FOLDER, "weather_" + name.lower() + ".csv")
            df.to_csv(filepath, index=False)
            print(f"  Rows: {len(df)}")
            print(f"  Saved: {filepath}")
            all_dfs.append(df)
        else:
            print(f"  FAILED: {r.text[:300]}")
            failed.append(name)

    except Exception as e:
        print(f"  ERROR: {e}")
        failed.append(name)

    if i < len(CITIES):
        time.sleep(2)

# Save master weather file
if all_dfs:
    master = pd.concat(all_dfs, ignore_index=True)
    master_path = os.path.join(RAW_FOLDER, "weather_all_cities.csv")
    master.to_csv(master_path, index=False)

    print("\n" + "=" * 50)
    print("WEATHER FETCH COMPLETE")
    print(f"Total rows    : {len(master):,}")
    print(f"Columns       : {list(master.columns)}")
    print(f"Cities done   : {len(all_dfs)}/10")
    if failed:
        print(f"Failed        : {', '.join(failed)}")
    print(f"Master file   : {master_path}")
    print("=" * 50)
else:
    print("NO DATA COLLECTED")