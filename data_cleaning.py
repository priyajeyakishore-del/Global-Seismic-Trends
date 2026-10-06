import pandas as pd
import numpy as np
import re
import sys

output_file = open(
    "data_cleaning_output.txt",
    "w",
    encoding="utf-8"
)

sys.stdout = output_file
# ============================================================
# LOAD RAW DATA
# ============================================================

df = pd.read_csv("raw_earthquake_data.csv")

print("=" * 70)
print("RAW DATA")
print("\n" + "=" * 70)

print("Rows:", len(df))
print("Columns:", len(df.columns))

# ============================================================
# CONVERT DATE/TIME COLUMNS
# ============================================================

df["time"] = pd.to_datetime(
    df["time"],
    unit="ms",
    errors="coerce"
)
df["updated"] = pd.to_datetime(
    df["updated"],
    unit="ms",
    errors="coerce"
)

# ============================================================
# TAKE A COPY OF THE DATAFRAME FOR CLEANING
# ============================================================

df_clean = df.copy()

# ============================================================
# DROP COMPLETELY EMPTY COLUMNS
# ============================================================
print("\n" + "=" * 80)
print("DROP COMPLETELY EMPTY COLUMNS")
print("\n" + "=" * 80)

empty_columns = [
    column
    for column in df_clean.columns
    if df_clean[column].isna().all()
]

print("\nCompletely empty columns:")
print(empty_columns)

df_clean = df_clean.drop(columns=empty_columns)

print("Columns after removing empty columns:", len(df_clean.columns))


# ============================================================
# HANDLE HIGH MISSING VALUES
# ============================================================

print("\n" + "=" * 80)
print("HANDLE HIGH MISSING VALUES")
print("\n" + "=" * 80)


# Check missing percentage
missing_percentage = (
    df_clean.isna().sum() / len(df_clean) * 100
).sort_values(ascending=False)

print("\nMissing value percentage:")
print(missing_percentage[missing_percentage > 0])

if "alert" in df_clean.columns:

    alert_missing_percentage = df_clean["alert"].isna().mean() * 100

    print(
        f"\nAlert column missing: "
        f"{alert_missing_percentage:.2f}%"
    )

    if alert_missing_percentage >= 90:

        print(
            "Alert column has very high missing values."
        )
        # Keep the column because alert analysis is part of the project requirements
    print(
            "Decision: KEEP alert column for specialized "
            "alert-level analysis."
        )

# ============================================================
# IMPUTE PARTIAL MISSING VALUES
# ============================================================
print("\n" + "=" * 80)
print("IMPUTE PARTIAL MISSING VALUES")
print("\n" + "=" * 80)
# ------------------------------------------------------------
# nst - Number of seismic stations
# ------------------------------------------------------------

print("\nImputing missing values for 'nst' column...")
if "nst" in df_clean.columns:

    nst_missing = df_clean["nst"].isna().sum()

    print(
        f"\nnst missing before: {nst_missing:,}"
    )

    df_clean["nst"] = df_clean["nst"].fillna(
        df_clean["nst"].median()
    )

    print(
        "nst missing after:",
        df_clean["nst"].isna().sum()
    )

# ------------------------------------------------------------
# dmin - Minimum distance to the nearest station
# ------------------------------------------------------------
print("\nImputing missing values for 'dmin' column...")
if "dmin" in df_clean.columns:

    dmin_missing = df_clean["dmin"].isna().sum()

    print(
        f"\ndmin missing before: {dmin_missing:,}"
    )

    df_clean["dmin"] = df_clean["dmin"].fillna(
        df_clean["dmin"].median()
    )

    print(
        "dmin missing after:",
        df_clean["dmin"].isna().sum()
    )

# ------------------------------------------------------------
# gap - Azimuthal gap
# ------------------------------------------------------------
print("\nImputing missing values for 'gap' column...")
if "gap" in df_clean.columns:

    gap_missing = df_clean["gap"].isna().sum()

    print(
        f"\ngap missing before: {gap_missing:,}"
    )

    df_clean["gap"] = df_clean["gap"].fillna(
        df_clean["gap"].median()
    )

    print(
        "gap missing after:",
        df_clean["gap"].isna().sum()
    )

# ============================================================
# RANGE & DOMAIN VALIDATION
# ============================================================

print("\n" + "=" * 80)
print("RANGE & DOMAIN VALIDATION")
print("\n" + "=" * 80)

# ------------------------------------------------------------
# Depth
# ------------------------------------------------------------
print("\nValidating depth values...")

if "depth_km" in df_clean.columns:

    negative_depth_count = (
        df_clean["depth_km"] < 0
    ).sum()

    print(
        f"\nNegative depth values: "
        f"{negative_depth_count:,}"
    )
    print(
        "Decision: Keep negative depth values for now, "
        "as they may represent valid geological phenomena."
    )
# ------------------------------------------------------------
# Remove impossible depth values
# ------------------------------------------------------------

if "depth_km" in df_clean.columns:

    impossible_depth = (
        df_clean["depth_km"] > 1000
    ).sum()

    print(
        f"Impossible depth values (>1000 km): "
        f"{impossible_depth:,}"
    )
    print("No impossible depth values found. No action needed.")

 # ------------------------------------------------------------
# Magnitude
# ------------------------------------------------------------
print("\nValidating magnitude values...")
if "mag" in df_clean.columns:

    invalid_mag = (
        (df_clean["mag"] < 2.5) |
        (df_clean["mag"] > 8.8)
    ).sum()

    print(
        f"Invalid magnitude values: "
        f"{invalid_mag:,}"
    )
    print("no invalid magnitude values found. No action needed.")

# ------------------------------------------------------------
# Latitude
# ------------------------------------------------------------
print("\nValidating latitude values...")
if "latitude" in df_clean.columns:

    invalid_latitude = (
        (df_clean["latitude"] < -90) |
        (df_clean["latitude"] > 90)
    ).sum()

    print(
        f"Invalid latitude values: "
        f"{invalid_latitude:,}"
    )
    print("No invalid latitude values found. No action needed.")

# ------------------------------------------------------------
# Longitude
# ------------------------------------------------------------
print("\nValidating longitude values...")
if "longitude" in df_clean.columns:

    invalid_longitude = (
        (df_clean["longitude"] < -180) |
        (df_clean["longitude"] > 180)
    ).sum()

    print(
        f"Invalid longitude values: "
        f"{invalid_longitude:,}"
    )
    print("No invalid longitude values found. No action needed.")


# ============================================================
# 7. OUTLIER ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("OUTLIER ANALYSIS")
print("\n" + "=" * 80)

outlier_columns = [
    "mag",
    "depth_km",
    "gap"
]

outlier_report = []

for column in outlier_columns:

    if column not in df_clean.columns:
        continue

    values = pd.to_numeric(
        df_clean[column],
        errors="coerce"
    ).dropna()

    if len(values) == 0:
        continue

    Q1 = values.quantile(0.25)
    Q3 = values.quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = (
        (values < lower_limit)
        |
        (values > upper_limit)
    )

    outlier_count = outliers.sum()

    outlier_percentage = (
        outlier_count / len(values) * 100
    )

    outlier_report.append({
        "Column": column,
        "Q1": round(Q1, 4),
        "Q3": round(Q3, 4),
        "IQR": round(IQR, 4),
        "Lower Limit": round(lower_limit, 4),
        "Upper Limit": round(upper_limit, 4),
        "Outlier Count": int(outlier_count),
        "Outlier %": round(outlier_percentage, 2)
    })

outlier_report_df = pd.DataFrame(
    outlier_report
)

print("\nIQR Outlier Detection Report:")

print(
    outlier_report_df.to_string(
        index=False
    )
)
print(
            "Decision: RETAIN statistical outliers "
            "because they may represent genuine "
            "earthquake characteristics."
        )

# ============================================================
# TEXT FIELD CLEANING
# ============================================================
print("\n" + "=" * 80)
print("TEXT FIELD CLEANING")
print("\n" + "=" * 80)

text_columns = [
    "status",
    "magType",
    "type",
    "net",
    "sources",
    "types"
]

for column in text_columns:

    if column in df_clean.columns:

        df_clean[column] = (
            df_clean[column]
            .astype("string")
            .str.lower()
            .str.strip()
        )

print("\nText field cleaning completed.")
print("Decision: RETAIN cleaned text fields for analysis.")

# ------------------------------------------------------------
# Clean place
# ------------------------------------------------------------

if "place" in df_clean.columns:

    df_clean["place"] = (
        df_clean["place"]
        .astype("string")
        .str.strip()
    )

print("\nPlace field cleaning completed.")

# ------------------------------------------------------------
# Extract country / region
# ------------------------------------------------------------

if "place" in df_clean.columns:

    df_clean["country"] = (
        df_clean["place"]
        .str.extract(
            r",\s*([^,]+)$",
            expand=False
        )
        .str.strip()
    )

    df_clean["country"] = (
        df_clean["country"]
        .fillna("Unknown")
    )
print("\nCountry field extraction completed.")
print("Decision: RETAIN country field for analysis.")
print("sample countries:", df_clean["country"].unique()[:10])

# ============================================================
# DERIVED FIELDS
# ============================================================

print("\n" + "=" * 80)
print("DERIVED FIELDS")
print("\n" + "=" * 80)
#number of columns before derived fields
print("Total columns before derived fields:", len(df_clean.columns))

# ------------------------------------------------------------
# Extract year, month, day, hour, and day of week from time
# ------------------------------------------------------------
df_clean["year"] = df_clean["time"].dt.year
df_clean["month"] = df_clean["time"].dt.month
df_clean["month_name"] = df_clean["time"].dt.month_name()
df_clean["day"] = df_clean["time"].dt.day
df_clean["day_of_week"] = df_clean["time"].dt.day_name()
df_clean["hour"] = df_clean["time"].dt.hour

print("\nDerived fields for year, month, day, hour, and day of week created.")
# number of columns after derived fields
print("Total columns after derived fields from time:", len(df_clean.columns))

# ------------------------------------------------------------
# Categorize depth into Shallow, Intermediate, and Deep
# ------------------------------------------------------------
df_clean["depth_category"] = np.select(
    [
        df_clean["depth_km"] < 50,
        df_clean["depth_km"].between(
            50,
            300,
            inclusive="left"
        ),
        df_clean["depth_km"] >= 300
    ],
    [
        "Shallow",
        "Intermediate",
        "Deep"
    ],
    default="Unknown"
)
print("\nDepth category derived field created.")
# number of columns after derived fields
print("Total columns after derived fields for depth:", len(df_clean.columns))

# ------------------------------------------------------------
# strong_quake: 1 if magnitude >= 7.5, else 0
# ------------------------------------------------------------
df_clean["strong_quake"] = np.where(
    df_clean["mag"] >= 7.5,
    1,
    0
)
print("\nStrong quake derived field created.")
# number of columns after derived fields
print("Total columns after derived fields for strong_quake:", len(df_clean.columns))

# ------------------------------------------------------------
# tsunami_indicator: "Yes" if tsunami == 1, else "No"
# ------------------------------------------------------------
if "tsunami" in df_clean.columns:

    df_clean["tsunami_indicator"] = np.where(
        df_clean["tsunami"] == 1,
        "Yes",
        "No"
    )
    print("\nTsunami indicator derived field created.")
    # number of columns after derived fields
    print("Total columns after derived fields for tsunami_indicator:", len(df_clean.columns))

# ----------------------------------------------------------------
# Categorize magnitude into Minor, Light, Moderate, Strong, Major
# ----------------------------------------------------------------
df_clean["magnitude_category"] = pd.cut(
    df_clean["mag"],
    bins=[
        0,
        4,
        5,
        6,
        7,
        10
    ],
    labels=[
        "Minor",
        "Light",
        "Moderate",
        "Strong",
        "Major"
    ],
    include_lowest=True
)
print("\nMagnitude category derived field created.")
print("Total columns after derived fields for magnitude_category:", len(df_clean.columns))

print("\nData cleaning and transformation completed.")

# ============================================================
# FINAL CLEANED DATA VALIDATION
# ============================================================
print("\n" + "=" * 80)
print("FINAL CLEANED DATA VALIDATION")
print("\n" + "=" * 80)
print("Final records:", f"{len(df_clean):,}") 
print("Final columns:", len(df_clean.columns))
print("duplicate rows:", df_clean.duplicated().sum())
print("missing values:", df_clean.isna().sum().sum())
print("timestamp range:", df_clean["time"].min(), "to", df_clean["time"].max())

print("\n" + "=" * 80)
print("✅ DATA CLEANING & TRANSFORMATION COMPLETED")
print("\n" + "=" * 80)


sys.stdout = sys.__stdout__
output_file.close()

print("Data cleaning & transformation completed.")
print("Output saved to data_cleaning_output.txt")

# Save the processed dataset
df_clean.to_csv("cleaned_earthquake_data.csv", index=False)

# verify the saved file
import os
if os.path.exists("cleaned_earthquake_data.csv"):
    print("\nFile saved successfully.\n")
else:
    print("\nFailed to save the file.\n")