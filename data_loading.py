import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import numpy as np

# Download earthquake data from USGS API for the period from September 2021 to September 2026

base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

start_date = datetime(2021, 9, 1)
end_date = datetime(2026, 9, 1)

all_features = []
current_date = start_date

while current_date < end_date:

    next_date = current_date + relativedelta(months=1)

    params = {
        "format": "geojson",
        "starttime": current_date.strftime("%Y-%m-%d"),
        "endtime": next_date.strftime("%Y-%m-%d"),
        "minmagnitude": 2.5,
        "orderby": "time-asc",
        "limit": 20000
    }

    response = requests.get(base_url, params=params, timeout=60)
    response.raise_for_status()

    data = response.json()
    features = data.get("features", [])

    all_features.extend(features)

    print(
        current_date.strftime("%Y-%m"),
        "->",
        len(features),
        "earthquakes"
    )

    if len(features) == 20000:
        print("WARNING: This month reached the API limit.")
        print("Split this month into smaller date ranges.")

    current_date = next_date
    time.sleep(0.2)

print("Total features downloaded:", len(all_features))

# Process the downloaded data into a DataFrame

records = []

for feature in all_features:

    properties = feature["properties"]
    coordinates = feature["geometry"]["coordinates"]

    longitude, latitude, depth = coordinates

    records.append({

        # 1. Unique earthquake identifier
        "id": feature.get("id"),

        # 2–3. Time information
        "time": properties.get("time"),
        "updated": properties.get("updated"),

        # 4–6. Geographic information
        "latitude": latitude,
        "longitude": longitude,
        "depth_km": depth,

        # 7–10. Earthquake information
        "mag": properties.get("mag"),
        "magType": properties.get("magType"),
        "place": properties.get("place"),
        "status": properties.get("status"),

        # 11–13. Impact / reporting information
        "tsunami": properties.get("tsunami"),
        "sig": properties.get("sig"),
        "net": properties.get("net"),

        # 14–17. Measurement quality
        "nst": properties.get("nst"),
        "dmin": properties.get("dmin"),
        "rms": properties.get("rms"),
        "gap": properties.get("gap"),

        # 18–20. Measurement errors
        "magError": properties.get("magError"),
        "depthError": properties.get("depthError"),
        "magNst": properties.get("magNst"),

        # 21–22. Source information
        "locationSource": properties.get("locationSource"),
        "magSource": properties.get("magSource"),

        # 23–26. Associated information
        "types": properties.get("types"),
        "ids": properties.get("ids"),
        "sources": properties.get("sources"),
        "type": properties.get("type"),
        "alert": properties.get("alert")
    })


# Create DataFrame
df = pd.DataFrame(records)


# Check dataset
print("\nDescription of the dataset:\n")
print("Dataset shape:", df.shape)
print("Number of columns:", len(df.columns))
print("First date:", df["time"].min())
print("Last date:", df["time"].max())

# Save the processed dataset
df.to_csv("raw_earthquake_data.csv", index=False)

# verify the saved file
import os
if os.path.exists("raw_earthquake_data.csv"):
    print("\nFile saved successfully.\n")
else:
    print("\nFailed to save the file.\n")


