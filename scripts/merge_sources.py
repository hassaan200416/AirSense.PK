# ============================================================
# AirSense PK — Final Merge: All 4 Sources
# ============================================================

import pandas as pd
import numpy as np
import os

RAW_FOLDER       = os.path.join("data", "raw")
PROCESSED_FOLDER = os.path.join("data", "processed")
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

print("=" * 60)
print("AIRSENSE PK — MERGING ALL 4 SOURCES")
print("=" * 60)

# ── Load Source 1: Open-Meteo Master ─────────────────────────
df_main = pd.read_csv(
    os.path.join(PROCESSED_FOLDER, "airsense_master_raw.csv"),
    parse_dates=["timestamp"]
)
print(f"\nSource 1 — Open-Meteo    : {len(df_main):,} rows")

# ── Load Source 2: WAQI ───────────────────────────────────────
df_waqi = pd.read_csv(os.path.join(RAW_FOLDER, "waqi_ground_sensors.csv"))
print(f"Source 2 — WAQI          : {len(df_waqi)} rows")

# ── Load Source 3: Kaggle ─────────────────────────────────────
df_kaggle = pd.read_csv(os.path.join(RAW_FOLDER, "kaggle_pakistan_aq.csv"))
print(f"Source 3 — Kaggle        : {len(df_kaggle):,} rows")

# ── Load Source 4: OpenAQ ─────────────────────────────────────
df_openaq = pd.read_csv(
    os.path.join(RAW_FOLDER, "openaq_measurements.csv"),
    parse_dates=["timestamp"]
)
print(f"Source 4 — OpenAQ        : {len(df_openaq):,} rows")

# ── OpenAQ Summary ────────────────────────────────────────────
print("\nOpenAQ Station Summary:")
station_summary = df_openaq.groupby("location_name").agg(
    measurements=("pm2_5", "count"),
    avg_pm25=("pm2_5", "mean"),
    min_date=("timestamp", "min"),
    max_date=("timestamp", "max")
).reset_index()
print(station_summary.to_string(index=False))

# ── Cross-Validation Table ────────────────────────────────────
print("\n" + "=" * 60)
print("CROSS-VALIDATION — Comparing PM2.5 Across Sources")
print("=" * 60)

our_10 = ["Lahore", "Karachi", "Islamabad", "Rawalpindi",
          "Faisalabad", "Peshawar", "Multan", "Quetta",
          "Gujranwala", "Hyderabad"]

kaggle_dict = {}
for _, r in df_kaggle.iterrows():
    if r["City"] in our_10:
        kaggle_dict[r["City"]] = r["PM2.5 AQI Value"]

waqi_dict = {r["city"]: r["pm25"] for _, r in df_waqi.iterrows()}

# Map OpenAQ stations to cities
openaq_city_map = {
    "Peshawar":                     "Peshawar",
    "Karachi":                      "Karachi",
    "US Diplomatic Post: Islamabad":"Islamabad",
    "US Diplomatic Post: Lahore":   "Lahore",
    "Islamabad":                    "Islamabad",
    "Karachi, Pakistan":            "Karachi",
    "Lahore":                       "Lahore",
}

openaq_dict = {}
for station, city in openaq_city_map.items():
    rows = df_openaq[df_openaq["location_name"] == station]["pm2_5"].dropna()
    if len(rows) > 0:
        openaq_dict[city] = round(rows.mean(), 1)

print(f"\n{'City':<15} {'OpenMeteo Median':<20} {'Kaggle AQI':<15} "
      f"{'WAQI Current':<15} {'OpenAQ Avg'}")
print("-" * 75)

for city in our_10:
    om  = df_main[df_main["city"] == city]["pm2_5"].median()
    kag = kaggle_dict.get(city, "N/A")
    waq = waqi_dict.get(city, "N/A")
    oaq = openaq_dict.get(city, "N/A")
    print(f"  {city:<13} {om:<20.1f} {str(kag):<15} "
          f"{str(waq):<15} {str(oaq)}")

# ── Save OpenAQ as Supplementary File ────────────────────────
print("\n" + "=" * 60)
print("SAVING PROCESSED FILES")
print("=" * 60)

# Save OpenAQ processed
openaq_processed = df_openaq.copy()
openaq_processed = openaq_processed.dropna(subset=["pm2_5"])
openaq_processed.to_csv(
    os.path.join(PROCESSED_FOLDER, "openaq_pakistan_processed.csv"),
    index=False
)
print(f"OpenAQ processed saved: {len(openaq_processed):,} rows "
      f"(after dropping NaN pm2_5)")

# ── Final Data Inventory ──────────────────────────────────────
print("\n" + "=" * 60)
print("COMPLETE DATA COLLECTION SUMMARY")
print("=" * 60)
print(f"{'Source':<30} {'Rows':>10} {'Columns':>10} {'Type'}")
print("-" * 70)
print(f"  {'Open-Meteo (primary)':<28} {len(df_main):>10,} "
      f"{df_main.shape[1]:>10} Satellite hourly 2022-2026")
print(f"  {'WAQI Ground Sensors':<28} {len(df_waqi):>10,} "
      f"{df_waqi.shape[1]:>10} Real sensor current readings")
print(f"  {'Kaggle Global AQ':<28} {len(df_kaggle):>10,} "
      f"{df_kaggle.shape[1]:>10} Published validated dataset")
print(f"  {'OpenAQ Pakistan':<28} {len(openaq_processed):>10,} "
      f"{df_openaq.shape[1]:>10} Ground sensors 100 stations")
print("-" * 70)
total = len(df_main) + len(df_waqi) + len(df_kaggle) + len(openaq_processed)
print(f"  {'TOTAL':<28} {total:>10,}")
print("\nAll sources complete. Ready for EDA.")
print("=" * 60)