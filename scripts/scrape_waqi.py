# ============================================================
# AirSense PK — Script 3: WAQI Ground Sensor Scraper
# Fetches real sensor readings from physical monitoring
# stations in Pakistani cities
# ============================================================

import requests
import pandas as pd
import os
import time

TOKEN = "c167899bdf7ec59366e89e6a3c3bddf748846ac1"

# Pakistani city station names as recognised by WAQI
# These are the exact slugs used by aqicn.org
STATIONS = [
    {"city": "Lahore",     "station": "lahore"},
    {"city": "Karachi",    "station": "karachi"},
    {"city": "Islamabad",  "station": "islamabad"},
    {"city": "Peshawar",   "station": "peshawar"},
    {"city": "Faisalabad", "station": "faisalabad"},
    {"city": "Multan",     "station": "multan"},
    {"city": "Quetta",     "station": "quetta"},
]

RAW_FOLDER = os.path.join("data", "raw")
os.makedirs(RAW_FOLDER, exist_ok=True)

print("=" * 55)
print("AirSense PK — WAQI Ground Sensor Scraper")
print(f"Token: {TOKEN[:8]}...")
print("=" * 55)

results = []

for s in STATIONS:
    city    = s["city"]
    station = s["station"]
    url     = f"https://api.waqi.info/feed/{station}/?token={TOKEN}"

    print(f"\nFetching: {city} (station: {station})")

    try:
        r = requests.get(url, timeout=30)
        data = r.json()

        if data["status"] == "ok":
            d = data["data"]
            iaqi = d.get("iaqi", {})

            row = {
                "city":             city,
                "station_name":     d.get("city", {}).get("name", ""),
                "timestamp":        d.get("time", {}).get("s", ""),
                "aqi":              d.get("aqi", None),
                "pm25":             iaqi.get("pm25", {}).get("v", None),
                "pm10":             iaqi.get("pm10", {}).get("v", None),
                "carbon_monoxide":  iaqi.get("co",   {}).get("v", None),
                "nitrogen_dioxide": iaqi.get("no2",  {}).get("v", None),
                "sulphur_dioxide":  iaqi.get("so2",  {}).get("v", None),
                "ozone":            iaqi.get("o3",   {}).get("v", None),
                "temperature":      iaqi.get("t",    {}).get("v", None),
                "humidity":         iaqi.get("h",    {}).get("v", None),
                "wind_speed":       iaqi.get("w",    {}).get("v", None),
                "pressure":         iaqi.get("p",    {}).get("v", None),
                "dominant_pollutant": d.get("dominentpol", ""),
                "data_source":      "WAQI_ground_sensor",
            }

            results.append(row)
            print(f"  OK — AQI: {row['aqi']}, PM2.5: {row['pm25']}, "
                  f"PM10: {row['pm10']}, Dominant: {row['dominant_pollutant']}")

        else:
            print(f"  FAILED — status: {data['status']}")
            print(f"  Response: {data}")

    except Exception as e:
        print(f"  ERROR: {e}")

    time.sleep(1)

# Save results
if results:
    df = pd.DataFrame(results)
    path = os.path.join(RAW_FOLDER, "waqi_ground_sensors.csv")
    df.to_csv(path, index=False)

    print("\n" + "=" * 55)
    print("WAQI SCRAPING COMPLETE")
    print(f"Stations fetched : {len(results)}")
    print(f"Saved            : {path}")
    print("=" * 55)
    print("\nFull data:")
    print(df.to_string(index=False))
else:
    print("\nNO DATA COLLECTED")