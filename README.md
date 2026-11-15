# Air Sense Project README

Air Sense is a Pakistan air-quality analysis project designed to understand pollution patterns, detect dangerous conditions, and prepare a data-driven foundation for forecasting and proposal writing. The project combines weather, ground sensor, satellite, and public AQI datasets to create one cleaner and more useful air-quality dataset for analysis.

This README is written in simple language so that even a person with no technical background can understand what was done and why it matters.

---

## 1. Project Goal

The goal of this project was to:

- collect air pollution and weather information from multiple sources,
- combine them into a single reliable dataset,
- clean missing or incorrect values,
- study pollution patterns across cities and seasons,
- identify the strongest indicators of poor air quality,
- prepare a final dataset and visual analysis suitable for proposal writing and model training.

In simple terms: we wanted to understand when air becomes unhealthy, which cities are most affected, and which factors best explain the pollution problem in Pakistan.

---

## 2. Why This Project Matters

Air pollution is a serious public health issue. In Pakistan, fine particulate matter like PM2.5 can cause respiratory diseases, heart problems, and reduced quality of life. This project helps turn raw air and weather data into understandable insights.

The final analysis focuses especially on:

- PM2.5 (very small particles harmful to health),
- PM10,
- carbon monoxide,
- nitrogen dioxide,
- sulphur dioxide,
- ozone,
- dust,
- weather conditions such as temperature, humidity, rainfall, wind, and pressure,
- AQI categories such as Good, Moderate, Unhealthy, and Hazardous.

---

## 3. Data Sources Used

The project combined four main data sources:

### 3.1 Open-Meteo

This was the primary dataset and included weather and environmental information. It formed the base of the project timeline and was the main source for many hourly measurements.

### 3.2 WAQI Ground Sensors

This provided ground-based air quality readings from real sensor stations. It helped verify local pollution conditions in different cities.

### 3.3 Kaggle Pakistan Air Quality Dataset

This provided published AQI information for Pakistan and helped validate city-level pollution trends.

### 3.4 OpenAQ Pakistan Measurements

This data contained ground-sensor measurements across Pakistan, including multiple stations and pollutant readings.

The raw data is stored in:

- data/raw/
- data/processed/
- data/external/

Examples of files included:

- data/raw/kaggle_pakistan_aq.csv
- data/raw/waqi_ground_sensors.csv
- data/raw/openaq_measurements.csv
- data/raw/openmeteo_lahore.csv
- data/raw/weather_all_cities.csv
- data/processed/airsense_master_raw.csv
- data/processed/airsense_final.csv

---

## 4. Project Workflow

The project followed a clear workflow:

1. Data collection from multiple air quality and weather sources.
2. Data merging and validation between sources.
3. Data cleaning and preprocessing.
4. Handling missing values and impossible readings.
5. Outlier treatment and feature engineering.
6. Exploratory data analysis (EDA).
7. Correlation and pattern discovery.
8. Summary reporting and proposal-ready findings.

This is the same structure used in the notebooks and scripts in the repository:

- notebooks/01_data_collection.ipynb
- notebooks/02_eda_raw.ipynb
- notebooks/03_preprocessing.ipynb
- notebooks/04_feature_engineering.ipynb
- notebooks/05_eda_clean.ipynb
- scripts/merge_sources.py
- scripts/scrape_openaq.py
- scripts/scrape_openmeteo.py
- scripts/scrape_waqi.py

---

## 5. What Was Done in the Data Cleaning Stage

The raw dataset had serious quality problems that had to be fixed before analysis. If these issues were left unchanged, the model and analysis would be misleading.

### 5.1 Missing values

The project found that a large number of pollutant readings were missing.

The EDA report states:

- 51,650 rows (12.1%) had no pollutant data,
- all missing pollutant values were concentrated in 2022 due to a structured satellite coverage gap,
- these values were resolved by city-wise median imputation.

This means instead of dropping a large number of rows, the project filled missing values using realistic city-specific medians.

### 5.2 Impossible negative values

The project discovered impossible negative pollutant readings, which are not physically realistic.

Exact values reported:

- 246 total negative readings were found,
- nitrogen dioxide: 17 negative values,
- ozone: 226 negative values,
- dust: 3 negative values.

These were treated as invalid values and converted to missing data before imputation.

### 5.3 Outlier handling

Extreme pollution spikes were also found. For example:

- PM2.5 had 27,948 IQR outliers,
- maximum raw PM2.5 value reached 486 µg/m³,
- the project winsorised values at 102.8 µg/m³ to cap extreme distortions while preserving real smog episodes.

This was critical because very high values can overwhelm a model and make the dataset look artificially extreme.

### 5.4 Cleaned dataset output

The final cleaned dataset is stored as:

- data/processed/airsense_final.csv

This file is the main final dataset used for the exploratory analysis and for downstream model preparation.

---

## 6. Feature Engineering and Data Enrichment

A major part of the project was not just cleaning, but creating more useful features.

The final data contains engineered variables such as:

- pollution_load_index (PLI),
- AQI category labels,
- aggregate pollution indicators,
- weather-adjusted pollution signals,
- city and time-based indicators.

The project notes that the engineered pollution load index is a valuable feature because it is highly related to AQI.

The final analysis mentions:

- 17 engineered features added after cleaning,
- the final dataset had significantly more usable information than the raw files.

---

## 7. Key EDA Findings (with Actual Values)

This is the most important section because it explains what the project actually discovered.

### 7.1 PM2.5 Distribution and air quality severity

The project compared raw and cleaned PM2.5 data.

Reported values include:

- PM2.5 max before preprocessing: 486 µg/m³,
- PM2.5 max after cleaning: capped at 102.8 µg/m³ through winsorisation,
- PM2.5 skewness before cleaning: 2.75,
- skewness was reduced significantly after cleaning and trimming of extreme values.

This shows that the cleaning logic successfully reduced the distortion caused by a few very extreme readings.

### 7.2 Correlation analysis

The cleaned dataset identified the strongest AQI-related variables.

Important findings:

- PM2.5 correlation with US AQI: 0.774,
- PM10 correlation with US AQI: 0.596,
- carbon monoxide correlation with US AQI: 0.508,
- wind speed correlation with US AQI: -0.272,
- pollution load index correlation with US AQI: 0.736.

This means PM2.5 is the strongest individual pollutant predictor of AQI. The pollution load index is also a strong engineered feature and is almost as informative as PM2.5.

### 7.3 Seasonal patterns

The project found clear seasonal differences in pollution.

- Winter PM2.5 mean: 68.78 µg/m³,
- Summer PM2.5 mean: 38.24 µg/m³,
- t-statistic: 151.56,
- p-value: p < 0.001.

This is a very strong indication that winter pollution is significantly worse than summer pollution.

### 7.4 City differences

The project also looked at city-to-city differences.

- Faisalabad median PM2.5: 56.2 µg/m³,
- Quetta median PM2.5: 15.5 µg/m³,
- ANOVA result: F = 12,493.94,
- p-value: p < 0.001.

This confirms that air quality differs significantly between cities in Pakistan.

### 7.5 Daily and hourly patterns

The project examined when pollution peaks during the day.

- PM2.5 peak period: 19:00 to 02:00,
- average peak PM2.5: 43.0 µg/m³,
- off-peak average: 33.6 µg/m³,
- difference: 9.4 µg/m³.

This suggests that pollution worsens during the evening and night, which may reflect local emissions patterns, weather conditions, and pollution buildup.

### 7.6 AQI category distribution

The final AQI category distribution was analyzed and the report notes a strong imbalance.

- Moderate AQI category: 41.9%,
- Hazardous AQI category: 0.3%.

This class imbalance is important because it affects model training. The project later notes that class weights may be needed to make the predictive model fair and effective.

---

## 8. Final Project Result

The project successfully created a clean, merged, and enriched dataset for air quality analysis in Pakistan.

The final summary in the notebook states:

- missing pollutant values were resolved,
- negative readings were corrected,
- outliers were handled,
- engineered features were added,
- AQI categories were classified,
- pollution trends were explained with evidence,
- the work is ready for proposal writing and model training.

The notebook ends with:

- "ALL EDA COMPLETE — READY FOR PROPOSAL WRITING AND MODEL TRAINING"

This means the project has reached a mature stage: the dataset is understandable, cleaned, and ready for further analytical or predictive work.

---

## 9. Main Files in the Project

### Data folders

- data/raw/
- data/processed/
- data/eda_plots/
- data/external/

### Notebook files

- notebooks/01_data_collection.ipynb
- notebooks/02_eda_raw.ipynb
- notebooks/03_preprocessing.ipynb
- notebooks/04_feature_engineering.ipynb
- notebooks/05_eda_clean.ipynb

### Scripts

- scripts/merge_sources.py
- scripts/scrape_openaq.py
- scripts/scrape_openmeteo.py
- scripts/scrape_waqi.py

### Final output dataset

- data/processed/airsense_final.csv
- data/processed/airsense_master_raw.csv
- data/processed/openaq_pakistan_processed.csv

---

## 10. What the Project Shows in Plain Language

If we summarize the whole project in one simple message:

> We collected air quality and weather information from several sources, cleaned the messy data, removed impossible values, fixed missing readings, and added useful pollution features. After analysis, we found that PM2.5 is the strongest indicator of bad air quality, winter is much worse than summer, different cities have very different pollution levels, and pollution spikes at night. These results make the project ready for deeper modeling, forecasting, and policy or proposal writing.

---

## 11. Final Takeaway

Air Sense is not just a dataset project; it is a full environmental data pipeline and exploratory analysis. It shows that raw air-quality data can be transformed into useful, evidence-based insight when cleaned properly and analyzed carefully.

The final output is a solid foundation for:

- further machine learning,
- air-quality prediction,
- city-wise monitoring,
- health risk analysis,
- policy recommendations,
- project or proposal reporting.

---

## 12. Short Summary

This project has:

- combined multiple air-quality sources,
- cleaned and corrected data issues,
- reduced noise and distortion from outliers,
- identified major pollution drivers,
- confirmed strong seasonal and city-level patterns,
- produced an analysis ready for future forecasting and reporting.

If you want, the next step can be to add a full project workflow diagram, a model-building section, or a more polished business-style executive summary for presentations.
