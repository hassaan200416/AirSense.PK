# ============================================================
# AirSense PK — Script 4: OpenAQ v3 Measurements
# Fixed endpoint for v3 API
# ============================================================

import requests
import pandas as pd
import os
import time

OPENAQ_KEY = "253aec447efb6748b39d94b7cfe707e7f14c7d23c01c9353aba56919c30104a8"
RAW_FOLDER = os.path.join("data", "raw")
os.makedirs(RAW_FOLDER, exist_ok=True)
headers = {"X-API-Key": OPENAQ_KEY}

print("=" * 60)
print("AirSense PK — OpenAQ v3 Measurements")
print("=" * 60)

# ── Step 1: Load saved Pakistan locations ────────────────────
locs_path = os.path.join(RAW_FOLDER, "openaq_pakistan_locations.csv")
df_locs   = pd.read_csv(locs_path)
print(f"Pakistan locations loaded: {len(df_locs)}")

# Focus on our 10 key cities — filter relevant stations
KEY_STATIONS = [
    "Lahore", "Karachi", "Islamabad", "Peshawar",
    "Rawalpindi", "Quetta", "Multan", "Faisalabad"
]

# ── Step 2: First test the correct v3 sensors endpoint ───────
print("\nStep 1: Testing correct v3 API endpoints...")

# Test with first location ID
first_id = df_locs["location_id"].iloc[0]
print(f"Testing location ID: {first_id}")

test_endpoints = [
    f"https://api.openaq.org/v3/sensors/{first_id}/measurements",
    f"https://api.openaq.org/v3/locations/{first_id}/sensors",
    f"https://api.openaq.org/v3/measurements?location_id={first_id}&limit=5",
]

working_endpoint = None
for ep in test_endpoints:
    r = requests.get(ep, headers=headers, timeout=30)
    print(f"  {ep}")
    print(f"  Status: {r.status_code}")
    if r.status_code == 200:
        print(f"  WORKS! Response preview: {r.text[:200]}")
        working_endpoint = ep
        break
    else:
        print(f"  Failed: {r.text[:100]}")

# ── Step 3: Get sensor IDs for each location ─────────────────
print("\nStep 2: Getting sensor IDs from locations...")
all_sensors = []

for _, loc in df_locs.iterrows():
    loc_id   = loc["location_id"]
    loc_name = loc["location_name"]

    sensor_url = f"https://api.openaq.org/v3/locations/{loc_id}/sensors"
    try:
        r = requests.get(sensor_url, headers=headers, timeout=30)
        if r.status_code == 200:
            sensors = r.json().get("results", [])
            for s in sensors:
                param = s.get("parameter", {})
                if param.get("name") in ["pm25", "pm2.5"]:
                    all_sensors.append({
                        "location_id":   loc_id,
                        "location_name": loc_name,
                        "sensor_id":     s.get("id"),
                        "parameter":     param.get("name"),
                        "unit":          param.get("units"),
                    })
                    print(f"  Found PM2.5 sensor at {loc_name}: sensor_id={s.get('id')}")
        else:
            print(f"  {loc_name}: {r.status_code}")
    except Exception as e:
        print(f"  {loc_name}: ERROR {e}")

    time.sleep(0.3)

print(f"\nTotal PM2.5 sensors found: {len(all_sensors)}")

if all_sensors:
    df_sensors = pd.DataFrame(all_sensors)
    sensors_path = os.path.join(RAW_FOLDER, "openaq_sensors.csv")
    df_sensors.to_csv(sensors_path, index=False)
    print(df_sensors.to_string(index=False))

    # ── Step 4: Fetch measurements using sensor IDs ──────────
    print("\nStep 3: Fetching measurements via sensor IDs...")
    all_measurements = []

    for _, sensor in df_sensors.iterrows():
        sensor_id = sensor["sensor_id"]
        loc_name  = sensor["location_name"]

        meas_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"
        params   = {
            "limit":        1000,
            "datetime_from": "2022-01-01T00:00:00Z",
            "datetime_to":   "2026-11-14T00:00:00Z",
        }

        try:
            r = requests.get(meas_url, headers=headers,
                           params=params, timeout=60)
            print(f"  Sensor {sensor_id} ({loc_name}): status {r.status_code}")

            if r.status_code == 200:
                meas = r.json().get("results", [])
                print(f"    Measurements returned: {len(meas)}")

                for m in meas:
                    period = m.get("period", {})
                    all_measurements.append({
                        "sensor_id":     sensor_id,
                        "location_name": loc_name,
                        "timestamp":     period.get("datetimeTo", {}).get("local", ""),
                        "pm2_5":         m.get("value"),
                        "data_source":   "OpenAQ_v3",
                    })
            else:
                print(f"    Failed: {r.text[:200]}")

        except Exception as e:
            print(f"    ERROR: {e}")

        time.sleep(0.5)

    if all_measurements:
        df_meas = pd.DataFrame(all_measurements)
        meas_path = os.path.join(RAW_FOLDER, "openaq_measurements.csv")
        df_meas.to_csv(meas_path, index=False)
        print(f"\nTotal measurements saved: {len(df_meas):,}")
        print(f"Saved: {meas_path}")
        print(df_meas.head(10).to_string(index=False))
    else:
        print("\nNo measurements collected via sensor endpoint")

print("\n" + "=" * 60)
print("OPENAQ COMPLETE")
print("=" * 60)