import pandas as pd
import numpy as np

import sys

output_file = open(
    "data_verification_output.txt",
    "w",
    encoding="utf-8"
)

sys.stdout = output_file
# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("raw_earthquake_data.csv")

# Convert the 'time' and 'updated' columns to datetime format
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


# Create a copy for validation
df_clean = df.copy()

# ============================================================
# 1. BASIC STRUCTURE CHECKS
# ============================================================

print("\n" + "=" * 80)
print("1. BASIC STRUCTURE CHECKS")
print("=" * 80)

print(f"Number of rows    : {df.shape[0]:,}")
print(f"Number of columns : {df.shape[1]:,}")

print("\nColumn names:")
for i, column in enumerate(df.columns, start=1):
    print(f"{i:2}. {column}")

print("\nDataFrame information:")
print(df.info())

# ============================================================
# 2. DATA TYPE VALIDATION
# ============================================================

print("\n" + "=" * 80)
print("2. DATA TYPE VALIDATION")
print("=" * 80)

# Expected data types based on the earthquake dataset
expected_dtypes = {

    # String columns
    "id": "string",
    "magType": "string",
    "place": "string",
    "status": "string",
    "net": "string",
    "types": "string",
    "ids": "string",
    "sources": "string",
    "type": "string",
    "alert": "string",

    # Datetime columns
    "time": "datetime",
    "updated": "datetime",

    # Numeric columns
    "latitude": "numeric",
    "longitude": "numeric",
    "depth_km": "numeric",
    "mag": "numeric",
    "nst": "numeric",
    "dmin": "numeric",
    "rms": "numeric",
    "gap": "numeric",

    # Integer columns
    "tsunami": "integer",
    "sig": "integer",

    # Columns currently containing no values
    "magError": "empty",
    "depthError": "empty",
    "magNst": "empty",
    "locationSource": "empty",
    "magSource": "empty"
}


# Create validation report
dtype_check = []

for column, expected_type in expected_dtypes.items():

    # Check whether column exists
    if column not in df.columns:

        dtype_check.append({
            "Column": column,
            "Expected Type": expected_type,
            "Actual Type": "Column Missing",
            "Non-Null": 0,
            "Valid": "No"
        })

        continue


    actual_dtype = df[column].dtype
    non_null_count = df[column].notna().sum()

# --------------------------------------------------------
    # String validation
    # --------------------------------------------------------

    if expected_type == "string":

        is_valid = (
            pd.api.types.is_object_dtype(df[column])
            or pd.api.types.is_string_dtype(df[column])
        )


    # --------------------------------------------------------
    # Datetime validation
    # --------------------------------------------------------

    elif expected_type == "datetime":

        is_valid = pd.api.types.is_datetime64_any_dtype(
            df[column]
        )


    # --------------------------------------------------------
    # Numeric validation
    # --------------------------------------------------------

    elif expected_type == "numeric":

        is_valid = pd.api.types.is_numeric_dtype(
            df[column]
        )


    # --------------------------------------------------------
    # Integer validation
    # --------------------------------------------------------

    elif expected_type == "integer":

        is_valid = pd.api.types.is_integer_dtype(
            df[column]
        )


    # --------------------------------------------------------
    # Empty column validation
    # --------------------------------------------------------

    elif expected_type == "empty":

        is_valid = df[column].isna().all()


    else:

        is_valid = False


    dtype_check.append({
        "Column": column,
        "Expected Type": expected_type,
        "Actual Type": str(actual_dtype),
        "Non-Null": non_null_count,
        "Valid": "Yes" if is_valid else "No"
    })


# Convert to DataFrame
dtype_check_df = pd.DataFrame(dtype_check)


# Display report
print(dtype_check_df.to_string(index=False))

# ============================================================
# 3. RANGE & DOMAIN CHECKS
# ============================================================

print("\n" + "=" * 80)
print("3️⃣ RANGE & DOMAIN CHECKS")
print("=" * 80)


# ------------------------------------------------------------
# Numeric Range Checks
# ------------------------------------------------------------

# Expected ranges
expected_ranges = {
    "latitude": (-90, 90),
    "longitude": (-180, 180),
    "depth_km": (-100, 1000),
    "mag": (-1, 10)
}

# Create data quality report
range_check = []

for column, (expected_min, expected_max) in expected_ranges.items():

    # Convert to numeric
    values = pd.to_numeric(df_clean[column], errors="coerce")

    actual_min = values.min()
    actual_max = values.max()

    # Check whether all non-null values are within the expected range
    is_valid = values.dropna().between(
        expected_min,
        expected_max
    ).all()

    # Count invalid values
    invalid_count = (
        (~values.between(expected_min, expected_max))
        & values.notna()
    ).sum()

    range_check.append({
        "Column": column,
        "Expected Range": f"{expected_min} to {expected_max}",
        "Actual Min": round(actual_min, 4),
        "Actual Max": round(actual_max, 4),
        "Invalid Values": invalid_count,
        "Valid": "Yes" if is_valid else "No"
    })

# Convert to DataFrame
range_check_df = pd.DataFrame(range_check)

print("\n" + "=" * 80)
print("🔢 NUMERIC RANGE VALIDATION REPORT")
print("=" * 80)

print(range_check_df.to_string(index=False))


# ------------------------------------------------------------
# Domain Checks
# ------------------------------------------------------------

print("\nDomain Validation:")

domain_checks = {}

if "tsunami" in df.columns:
    valid_tsunami = df["tsunami"].dropna().isin([0, 1]).all()
    domain_checks["tsunami"] = valid_tsunami

if "status" in df.columns:
    valid_status = df["status"].dropna().isin(
        ["automatic", "reviewed"]
    ).all()
    domain_checks["status"] = valid_status

if "magType" in df.columns:
    domain_checks["magType"] = df["magType"].notna().all()

for column, result in domain_checks.items():
    print(
        f"{'✅' if result else '❌'} "
        f"{column}: {'Valid' if result else 'Invalid'}"
    )


# ============================================================
# 4. MISSING VALUES
# ============================================================

print("\n" + "=" * 80)
print("4️⃣ MISSING VALUES")
print("=" * 80)

missing_count = df.isnull().sum()

missing_percentage = (
    missing_count / len(df) * 100
).round(2)

missing_report = pd.DataFrame({
    "Column": missing_count.index,
    "Missing Count": missing_count.values,
    "Missing %": missing_percentage.values
})

missing_report = missing_report[
    missing_report["Missing Count"] > 0
].sort_values(
    "Missing Count",
    ascending=False
)

if missing_report.empty:

    print("✅ No missing values found.")

else:

    print(
        missing_report.to_string(index=False)
    )


# ============================================================
# 5. CONSISTENCY CHECKS
# ============================================================

print("\n" + "=" * 80)
print("5️⃣ CONSISTENCY CHECKS")
print("=" * 80)


# ------------------------------------------------------------
#  Duplicate Rows
# ------------------------------------------------------------

duplicate_rows = df.duplicated().sum()

print(
    f"Duplicate rows          : {duplicate_rows:,}"
)

if duplicate_rows == 0:
    print("✅ No duplicate rows found.")
else:
    print("⚠️ Duplicate rows found.")


# ------------------------------------------------------------
# Duplicate Earthquake IDs
# ------------------------------------------------------------

if "id" in df.columns:

    duplicate_ids = df["id"].duplicated().sum()

    print(
        f"Duplicate earthquake IDs: {duplicate_ids:,}"
    )

    if duplicate_ids == 0:
        print("✅ Earthquake IDs are unique.")
    else:
        print("⚠️ Duplicate earthquake IDs found.")

# ------------------------------------------------------------
# Time Consistency
# ------------------------------------------------------------

if "time" in df.columns:

    time_values = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

    invalid_dates = time_values.isna().sum()

    print(
        f"Invalid date/time values: {invalid_dates:,}"
    )

    if invalid_dates == 0:
        print("✅ All date/time values are valid.")
    else:
        print("⚠️ Invalid date/time values found.")


# ------------------------------------------------------------
# Updated Time >= Event Time
# ------------------------------------------------------------

if "time" in df.columns and "updated" in df.columns:

    event_time = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

    updated_time = pd.to_datetime(
        df["updated"],
        errors="coerce"
    )

    invalid_updated = (
        updated_time < event_time
    ).sum()

    print(
        f"Updated before event time: {invalid_updated:,}"
    )

    if invalid_updated == 0:
        print("✅ Event/update timestamps are consistent.")
    else:
        print("⚠️ Some update timestamps occur before event time.")

# ------------------------------------------------------------
# Magnitude / Depth Consistency
# ------------------------------------------------------------

if "mag" in df.columns and "depth_km" in df.columns:

    missing_mag_depth = (
        df["mag"].isna() &
        df["depth_km"].isna()
    ).sum()

    print(
        f"Records missing both magnitude and depth: "
        f"{missing_mag_depth:,}"
    )

    if missing_mag_depth == 0:
        print("✅ Magnitude/depth availability is consistent.")
    else:
        print("⚠️ Records missing both magnitude and depth found.")

# ------------------------------------------------------------
# Geographic Consistency
# ------------------------------------------------------------

if "latitude" in df.columns and "longitude" in df.columns:

    invalid_coordinates = (
        (~df["latitude"].between(-90, 90))
        |
        (~df["longitude"].between(-180, 180))
    ).sum()

    print(
        f"Invalid geographic coordinates: {invalid_coordinates:,}"
    )

    if invalid_coordinates == 0:
        print("✅ Geographic coordinates are valid.")
    else:
        print("⚠️ Invalid geographic coordinates found.")

# ============================================================
# 6️⃣ OUTLIER DETECTION
# ============================================================

print("\n" + "=" * 80)
print("6️⃣ OUTLIER DETECTION")
print("=" * 80)


# ------------------------------------------------------------
# IQR Method
# ------------------------------------------------------------


outlier_columns = [
    "mag",
    "depth_km",
    "gap"
]

outlier_report = []

for column in outlier_columns:

    if column not in df.columns:
        continue

    values = pd.to_numeric(
        df[column],
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

# ============================================================
# 7️⃣ RECORD COUNT VERIFICATION
# ============================================================

print("\n" + "=" * 80)
print("7️⃣ RECORD COUNT VERIFICATION")
print("=" * 80)


# Total records
total_records = len(df)

print(
    f"Total records in dataset: {total_records:,}"
)


# Unique IDs
if "id" in df.columns:

    unique_ids = df["id"].nunique()

    print(
        f"Unique earthquake IDs    : {unique_ids:,}"
    )

    if total_records == unique_ids:

        print(
            "✅ Record count matches unique earthquake IDs."
        )

    else:

        difference = total_records - unique_ids

        print(
            f"⚠️ Difference between records and unique IDs: "
            f"{difference:,}"
        )


# ------------------------------------------------------------
# Records by Year
# ------------------------------------------------------------

if "time" in df.columns:

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

    yearly_counts = (
        df["time"]
        .dt.year
        .value_counts()
        .sort_index()
    )

    print("\nEarthquake records by year:")

    print(
        yearly_counts.to_string()
    )



# ------------------------------------------------------------
# 10. Overall Data Quality Conclusion
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("🎯 OVERALL DATA QUALITY CONCLUSION")
print("=" * 80)

print(
    f"""
The raw earthquake dataset contains {len(df):,} records
and {len(df.columns)} columns.

The validation process checked:

✓ Dataset structure
✓ Data types
✓ Geographic and magnitude ranges
✓ Domain values
✓ Missing values
✓ Duplicate records and IDs
✓ Timestamp consistency
✓ Magnitude/depth availability
✓ Geographic coordinates
✓ Statistical outliers using IQR
✓ Record counts and yearly distribution

The identified missing values, empty fields and statistical
outliers should be investigated during the data-cleaning stage.

"""
)

print("=" * 80)
print("✅ DATA QUALITY VALIDATION COMPLETED")
print("=" * 80)


sys.stdout = sys.__stdout__
output_file.close()

print("Data verification completed.")
print("Output saved to data_verification_output.txt")