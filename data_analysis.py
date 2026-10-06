import sys

import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

output_file = open(
    "sql_analysis_output.txt",
    "w",
    encoding="utf-8"
)

sys.stdout = output_file
# ============================================================
# DATABASE CONNECTION
# ============================================================

password = "Dinnu@world"

engine = create_engine(
    f"mysql+pymysql://root:{quote_plus(password)}@localhost:3306/earthquake_db"
)


# ============================================================
# HELPER FUNCTION TO RUN SQL QUERIES
# ============================================================

def run_query(engine, query):
    """
    Execute a SQL query and return the result
    as a Pandas DataFrame.
    """

    with engine.connect() as conn:

        result = conn.execute(text(query))

        return pd.DataFrame(
            result.fetchall(),
            columns=result.keys()
        )

# ============================================================
# HELPER FUNCTION TO DISPLAY RESULTS
# ============================================================

def display_result(title, df):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    print(df)


# ============================================================
# BASIC DATASET INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("BASIC DATASET INFORMATION")
print("=" * 60)

# ============================================================
# 1. TOTAL NUMBER OF EARTHQUAKES
# ============================================================

def get_total_earthquakes(engine):
    """
    Return the total number of earthquake records.
    """

    query = """
    SELECT COUNT(*) AS total_earthquakes
    FROM cleaned_earthquake_data
    """

    return run_query(engine, query)


# Test the function
df = get_total_earthquakes(engine)

print(
    "total_earthquakes:",
    df.iloc[0]["total_earthquakes"]
)
# ============================================================
# 2. STRONGEST EARTHQUAKE
# ============================================================

def get_strongest_magnitude(engine):
    """
    Return the strongest earthquake magnitude.
    """

    query = """
    SELECT MAX(mag) AS strongest_magnitude
    FROM cleaned_earthquake_data
    WHERE mag IS NOT NULL
    """

    return run_query(engine, query)
# Test the function
df = get_strongest_magnitude(engine)

print(
    "strongest_magnitude:",df.iloc[0]["strongest_magnitude"]
)
# ============================================================
# 3. DEEPEST EARTHQUAKE
# ============================================================

def get_deepest_earthquake(engine):
    """
    Return the deepest earthquake depth in kilometers.
    """

    query = """
    SELECT MAX(depth_km) AS deepest_depth
    FROM cleaned_earthquake_data
    WHERE depth_km IS NOT NULL
    """

    return run_query(engine, query)
df = get_deepest_earthquake(engine)
print(
    "deepest_depth:",df.iloc[0]["deepest_depth"]
)
# ============================================================
# 4. TOTAL TSUNAMI-ASSOCIATED EARTHQUAKES
# ============================================================

def get_total_tsunamis(engine):
    """
    Return the number of earthquakes associated
    with tsunami indicators.
    """

    query = """
    SELECT COUNT(*) AS total_tsunamis
    FROM cleaned_earthquake_data
    WHERE tsunami = 1
    """

    return run_query(engine, query)
print(
    "total_tsunamis:",get_total_tsunamis(engine).iloc[0]["total_tsunamis"]
)


print("\n"+"=" * 60 )
print("DATA ANALYSIS TASK")
print("=" * 60 + "\n")

print("\n * Magnitude & Depth Analysis * \n")
# ============================================================
# 1. TOP 10 STRONGEST EARTHQUAKES
# ============================================================

def get_top_10_strongest_earthquakes(engine):
    """
    Return the top 10 strongest earthquakes
    based on magnitude.
    """

    query = """
    SELECT id, time, country, mag, depth_km
    FROM cleaned_earthquake_data
    WHERE mag IS NOT NULL
    ORDER BY mag DESC
    LIMIT 10
    """

    return run_query(engine, query)

df_top_10_strongest = get_top_10_strongest_earthquakes(engine)

display_result(
    "1. TOP 10 STRONGEST EARTHQUAKES",
    df_top_10_strongest
)

# ============================================================
# 2. TOP 10 DEEPEST EARTHQUAKES
# ============================================================


def get_top_10_deepest_earthquakes(engine):
    """
    Return the top 10 deepest earthquakes based on depth in kilometers.
    """

    query = """
    SELECT id, time, country, mag, depth_km
    FROM cleaned_earthquake_data
    WHERE depth_km IS NOT NULL
    ORDER BY depth_km DESC
    LIMIT 10
    """

    return run_query(engine, query)

df_top_10_deepest = get_top_10_deepest_earthquakes(engine)

display_result(
    "2. TOP 10 DEEPEST EARTHQUAKES",
    df_top_10_deepest
)

# ============================================================
# 3. SHALLOW EARTHQUAKES < 50 KM AND MAG > 7.5
# ============================================================

def get_shallow_strong_earthquakes(engine):
    """
    Get shallow earthquakes with magnitude greater than 7.5.
    """

    query = """
    SELECT
        id,
        mag,
        depth_km,
        place,
        country,
        time
    FROM cleaned_earthquake_data
    WHERE depth_km < 50
      AND mag > 7.5
    ORDER BY mag DESC
    """

    return run_query(engine, query)
df_shallow_strong = get_shallow_strong_earthquakes(engine)

display_result(
    "3. SHALLOW EARTHQUAKES (< 50 KM) WITH MAGNITUDE > 7.5",
    df_shallow_strong
)
# ============================================================
# 5. AVERAGE MAGNITUDE PER MAGNITUDE TYPE
# ============================================================
def get_average_magnitude_per_mag_type(engine):
    """
    Get the average magnitude for each magnitude type.
    """
    query = """
    SELECT
        magType,
        COUNT(*) AS earthquake_count,
        ROUND(AVG(mag), 2) AS average_magnitude
    FROM cleaned_earthquake_data
    WHERE magType IS NOT NULL
    AND mag IS NOT NULL
    GROUP BY magType
    ORDER BY average_magnitude DESC
    """

    return run_query(engine, query)
df_avg_mag_type = get_average_magnitude_per_mag_type(engine)

display_result(
    "5. AVERAGE MAGNITUDE PER MAGNITUDE TYPE",
    df_avg_mag_type
)

print("\n * Time Analysis * \n")

# ============================================================
# 6. YEAR WITH MOST EARTHQUAKES
# ============================================================
def get_year_with_most_earthquakes(engine):
    """
    Get the year with the highest number of earthquakes.
    """
    query = """
    SELECT
        YEAR(time) AS year,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE time IS NOT NULL
    GROUP BY YEAR(time)
    ORDER BY earthquake_count DESC
    LIMIT 1
    """
    return run_query(engine, query)
df_year_most = get_year_with_most_earthquakes(engine)

display_result(
    "6. YEAR WITH MOST EARTHQUAKES",
    df_year_most
)

# ============================================================
# 7. MONTH WITH HIGHEST NUMBER OF EARTHQUAKES
# ============================================================
def get_month_with_most_earthquakes(engine):
    """
    Get the month with the highest number of earthquakes.
    """
    query = """
    SELECT
        MONTH(time) AS month_number,
        MONTHNAME(time) AS month_name,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE time IS NOT NULL
    GROUP BY MONTH(time), MONTHNAME(time)
    ORDER BY earthquake_count DESC
    LIMIT 1
    """
    return run_query(engine, query)
df_month_most = get_month_with_most_earthquakes(engine)

display_result(
    "7. MONTH WITH HIGHEST NUMBER OF EARTHQUAKES",
    df_month_most
)


# ============================================================
# 8. DAY OF WEEK WITH MOST EARTHQUAKES
# ============================================================
def get_day_with_most_earthquakes(engine):
    """
    Get the day of the week with the highest number of earthquakes.
    """
    query = """
    SELECT
        DAYNAME(time) AS day_of_week,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE time IS NOT NULL
    GROUP BY DAYOFWEEK(time), DAYNAME(time)
    ORDER BY earthquake_count DESC
    LIMIT 1
    """
    return run_query(engine, query)
df_day_most = get_day_with_most_earthquakes(engine)

display_result(
    "8. DAY OF WEEK WITH MOST EARTHQUAKES",
    df_day_most
)
# ============================================================
# 9. EARTHQUAKES PER HOUR
# ============================================================
def get_earthquakes_per_hour(engine):
    """
    Get the number of earthquakes for each hour of the day.
    """
    query = """
    SELECT
        HOUR(time) AS hour_of_day,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE time IS NOT NULL
    GROUP BY HOUR(time)
    ORDER BY hour_of_day
    """
    return run_query(engine, query)
df_hourly = get_earthquakes_per_hour(engine)

display_result(
    "9. EARTHQUAKES PER HOUR",
    df_hourly
)



# ============================================================
# 10. MOST ACTIVE REPORTING NETWORK
# ============================================================
def get_most_active_reporting_network(engine):
    """
    Get the reporting network with the highest number of earthquakes.
    """
    query = """
    SELECT
        net,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE net IS NOT NULL
    GROUP BY net
    ORDER BY earthquake_count DESC
    LIMIT 1
    """

    return run_query(engine, query)

df_network = get_most_active_reporting_network(engine)

display_result(
    "10. MOST ACTIVE REPORTING NETWORK",
    df_network
)

print("\n * Event Type & Quality Metrics * \n")

# ============================================================
# 14. REVIEWED VS AUTOMATIC
# ============================================================
def get_reviewed_vs_automatic(engine):
    """
    Get the count of earthquakes based on their review status.
    """
    query = """
    SELECT
        status,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE status IS NOT NULL
    GROUP BY status
    ORDER BY earthquake_count DESC
    """

    return run_query(engine, query)

df_status = get_reviewed_vs_automatic(engine)

display_result(
    "14. REVIEWED VS AUTOMATIC EARTHQUAKES",
    df_status
)

# ============================================================
# 15. COUNT BY EARTHQUAKE TYPE
# ============================================================
def get_count_by_earthquake_type(engine):
    """
    Get the count of earthquakes grouped by their type.
    """
    query = """
    SELECT
        type,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE type IS NOT NULL
    GROUP BY type
    ORDER BY earthquake_count DESC
    """

    return run_query(engine, query)

df_type = get_count_by_earthquake_type(engine)

display_result(
    "15. COUNT BY EARTHQUAKE TYPE",
    df_type
)

# ============================================================
# 16. NUMBER OF EARTHQUAKES BY DATA TYPE
# ============================================================
def get_count_by_data_type(engine):
    """
    Get the count of earthquakes grouped by their data type.
    """
    query = """
    SELECT
        types,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE types IS NOT NULL
    GROUP BY types
    ORDER BY earthquake_count DESC
    """

    return run_query(engine, query)

df_types = get_count_by_data_type(engine)

display_result(
    "16. NUMBER OF EARTHQUAKES BY DATA TYPE",
    df_types
)

# ============================================================
# 18. HIGH STATION COVERAGE
# ============================================================
def get_high_station_coverage(engine):
    """
    Get earthquakes with high station coverage
    where NST is greater than the 75th percentile.
    """

    # Step 1: Get all non-null NST values
    nst_query = """
    SELECT nst
    FROM cleaned_earthquake_data
    WHERE nst IS NOT NULL
    """

    df_nst = run_query(engine, nst_query)

    # Step 2: Calculate 75th percentile
    station_threshold = df_nst["nst"].quantile(0.75)

    # Step 3: Get earthquakes above the 75th percentile
    query = f"""
    SELECT
        id,
        nst,
        mag,
        country,
        time
    FROM cleaned_earthquake_data
    WHERE nst > {station_threshold}
    ORDER BY nst DESC
    """

    # Step 4: Return DataFrame and threshold
    df_high_station = run_query(engine, query)

    return df_high_station, station_threshold

df_high_station, station_threshold = get_high_station_coverage(engine)
display_result(
    f"18. EVENTS WITH HIGH STATION COVERAGE (NST > {station_threshold:.2f})",
    df_high_station
)

print(f"75th percentile (Q3) of NST: {station_threshold:.2f}")


print("\n * Tsunamis & Alerts * \n")

# ============================================================
# 19. TSUNAMIS PER YEAR
# ============================================================
def get_tsunamis_per_year(engine):
    """
    Get the number of tsunamis triggered per year.
    """
    query = """
    SELECT
        YEAR(time) AS year,
        COUNT(*) AS tsunami_count
    FROM cleaned_earthquake_data
    WHERE tsunami = 1
    AND time IS NOT NULL
    GROUP BY YEAR(time)
    ORDER BY year
    """

    df_tsunami_year = run_query(engine, query)

    return df_tsunami_year

df_tsunami_year = get_tsunamis_per_year(engine)

display_result(
    "19. TSUNAMIS TRIGGERED PER YEAR",
    df_tsunami_year
)

# ============================================================
# 20. EARTHQUAKES BY ALERT LEVEL
# ============================================================
def get_earthquakes_by_alert_level(engine):
    """
    Get the count of earthquakes grouped by their alert level.
    """
    query = """
    SELECT
        alert,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE alert IS NOT NULL
    GROUP BY alert
    ORDER BY earthquake_count DESC;
    """

    df_alert = run_query(engine, query)

    return df_alert

df_alert = get_earthquakes_by_alert_level(engine)

display_result(
    "20. EARTHQUAKES BY ALERT LEVEL",
    df_alert
)

print("\n * Seismic Pattern & Trends Analysis. * \n")
# ============================================================
# 21. TOP 5 COUNTRIES BY AVERAGE MAGNITUDE - PAST 5 YEARS
# ============================================================
def get_top_5_countries_by_avg_magnitude(engine):
    """
    Get the top 5 countries with the highest average earthquake magnitude
    over the past 5 years.
    """
    query = """
    SELECT
        country,
        ROUND(AVG(mag), 2) AS average_magnitude,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE time >= DATE_SUB(
        (SELECT MAX(time) FROM cleaned_earthquake_data),
        INTERVAL 5 YEAR
    )
    AND country IS NOT NULL
    AND mag IS NOT NULL
    GROUP BY country
    ORDER BY average_magnitude DESC
    LIMIT 5;
    """

    return run_query(engine, query)

df_top_countries_mag = get_top_5_countries_by_avg_magnitude(engine)

display_result(
    "21. TOP 5 COUNTRIES BY AVERAGE MAGNITUDE - PAST 5 YEARS",
    df_top_countries_mag
)
# ============================================================
# 22. COUNTRIES WITH BOTH SHALLOW AND DEEP EARTHQUAKES
#     IN THE SAME MONTH
# ============================================================

def get_countries_with_shallow_deep_same_month(engine):
    """
    Get countries that have both shallow and deep earthquakes
    in the same month, along with their shallow and deep depths.
    """

    query = """
    SELECT
        country,
        year,
        month,
        MIN(
            CASE
                WHEN depth_category = 'Shallow'
                THEN depth_km
            END
        ) AS shallow_depth_km,
        MAX(
            CASE
                WHEN depth_category = 'Deep'
                THEN depth_km
            END
        ) AS deep_depth_km
    FROM (
        SELECT
            country,
            YEAR(time) AS year,
            MONTH(time) AS month,
            depth_category,
            depth_km
        FROM cleaned_earthquake_data
        WHERE country IS NOT NULL
          AND country <> 'Unknown'
          AND time IS NOT NULL
          AND depth_km IS NOT NULL
          AND depth_category IS NOT NULL
    ) AS monthly_data

    GROUP BY
        country,
        year,
        month

    HAVING
        SUM(
            CASE
                WHEN depth_category = 'Shallow'
                THEN 1
                ELSE 0
            END
        ) > 0
        AND
        SUM(
            CASE
                WHEN depth_category = 'Deep'
                THEN 1
                ELSE 0
            END
        ) > 0

    ORDER BY
        country,
        year,
        month;
    """

    return run_query(engine, query)
df_shallow_deep_same_month = get_countries_with_shallow_deep_same_month(engine)

display_result(
    "22. COUNTRIES WITH BOTH SHALLOW AND DEEP EARTHQUAKES IN SAME MONTH",
    df_shallow_deep_same_month
)

# ============================================================
# 23. YEAR-OVER-YEAR GROWTH RATE
# ============================================================
def get_year_over_year_growth_rate(engine):
    """
    Calculate the year-over-year growth rate of earthquakes.
    """
    query = """
    SELECT
        year,
        earthquake_count,
        ROUND(
            (earthquake_count - LAG(earthquake_count) OVER (ORDER BY year))
            / LAG(earthquake_count) OVER (ORDER BY year) * 100,
            2
        ) AS yoy_growth_rate
    FROM (
        SELECT
            YEAR(time) AS year,
            COUNT(*) AS earthquake_count
        FROM cleaned_earthquake_data
        GROUP BY YEAR(time)
    ) AS yearly_counts
    ORDER BY year;
    """

    return run_query(engine, query)

df_yoy = get_year_over_year_growth_rate(engine)

display_result(
    "23. YEAR-OVER-YEAR EARTHQUAKE GROWTH RATE",
    df_yoy
)

# ============================================================
# 24. TOP 3 SEISMICALLY ACTIVE REGIONS
#     FREQUENCY + AVERAGE MAGNITUDE
# ============================================================

def get_top_3_active_regions(engine):
    """
    Get the top 3 seismically active countries
    based on earthquake frequency and average magnitude.
    """

    query = """
    SELECT
        country,
        COUNT(*) AS earthquake_count,
        ROUND(AVG(mag), 2) AS average_magnitude
    FROM cleaned_earthquake_data
    WHERE country IS NOT NULL
      AND country <> 'Unknown'
      AND mag IS NOT NULL
    GROUP BY country
    ORDER BY
        earthquake_count DESC,
        average_magnitude DESC
    LIMIT 3;
    """

    return run_query(engine, query)

df_active_regions = get_top_3_active_regions(engine)

display_result(
    "24. TOP 3 SEISMICALLY ACTIVE REGIONS",
    df_active_regions
)

print("\n * Depth, Location & Distance-Based  Analysis. * \n")
# ============================================================
# 25. AVERAGE DEPTH WITHIN ±5° OF EQUATOR
# ============================================================

def get_average_depth_near_equator(engine):
    """
    Get the average earthquake depth by country
    within ±5° latitude of the Equator.
    """

    query = """
    SELECT
        country,
        ROUND(AVG(depth_km), 2) AS average_depth_km
    FROM cleaned_earthquake_data
    WHERE latitude BETWEEN -5 AND 5
      AND country IS NOT NULL
      AND country <> 'Unknown'
      AND depth_km IS NOT NULL
    GROUP BY country
    ORDER BY average_depth_km DESC;
    """

    return run_query(engine, query)

df_equator_depth = get_average_depth_near_equator(engine)

display_result(
    "25. AVERAGE DEPTH BY COUNTRY WITHIN ±5° LATITUDE OF EQUATOR",
    df_equator_depth
)
# ============================================================
# 26. COUNTRIES WITH HIGHEST SHALLOW/DEEP RATIO
# ============================================================

def get_highest_shallow_deep_ratio(engine):
    """
    Get countries with the highest ratio of
    shallow earthquakes to deep earthquakes.
    """

    query = """
    SELECT
        country,

        SUM(
            CASE
                WHEN depth_category = 'Shallow' THEN 1
                ELSE 0
            END
        ) AS shallow_earthquakes,

        SUM(
            CASE
                WHEN depth_category = 'Deep' THEN 1
                ELSE 0
            END
        ) AS deep_earthquakes,

        ROUND(
            SUM(
                CASE
                    WHEN depth_category = 'Shallow' THEN 1
                    ELSE 0
                END
            )
            /
            SUM(
                CASE
                    WHEN depth_category = 'Deep' THEN 1
                    ELSE 0
                END
            ),
            2
        ) AS shallow_to_deep_ratio

    FROM cleaned_earthquake_data

    WHERE country IS NOT NULL
      AND country <> 'Unknown'
      AND depth_category IS NOT NULL

    GROUP BY country

    HAVING
        SUM(
            CASE
                WHEN depth_category = 'Deep' THEN 1
                ELSE 0
            END
        ) > 0

    ORDER BY shallow_to_deep_ratio DESC;
    """

    return run_query(engine, query)
df_shallow_deep_ratio = get_highest_shallow_deep_ratio(engine)

display_result(
    "26. COUNTRIES WITH HIGHEST SHALLOW/DEEP EARTHQUAKE RATIO",
    df_shallow_deep_ratio
)
# ============================================================
# 27. AVERAGE MAGNITUDE DIFFERENCE
#     TSUNAMI VS NON-TSUNAMI
# ============================================================

def get_average_magnitude_tsunami_difference(engine):
    """
    Compare the average earthquake magnitude between
    tsunami and non-tsunami events.
    """

    query = """
    SELECT
        ROUND(
            AVG(CASE WHEN tsunami = 1 THEN mag END),
            2
        ) AS avg_mag_with_tsunami,

        ROUND(
            AVG(CASE WHEN tsunami = 0 THEN mag END),
            2
        ) AS avg_mag_without_tsunami,

        ROUND(
            AVG(CASE WHEN tsunami = 1 THEN mag END)
            -
            AVG(CASE WHEN tsunami = 0 THEN mag END),
            2
        ) AS average_magnitude_difference

    FROM cleaned_earthquake_data

    WHERE mag IS NOT NULL
      AND tsunami IN (0, 1);
    """

    return run_query(engine, query)

df_avg_mag_diff = get_average_magnitude_tsunami_difference(engine)

display_result(
    "27. AVERAGE MAGNITUDE DIFFERENCE: TSUNAMI VS NON-TSUNAMI",
    df_avg_mag_diff
)
# ============================================================
# 28. LOWEST DATA RELIABILITY
#     HIGH RMS + HIGH GAP
# ============================================================

def get_lowest_data_reliability(engine):
    """
    Get events with the highest reliability error score,
    based on RMS and GAP values.
    """

    query = """
    SELECT
        id,
        place,
        country,
        mag,
        rms,
        gap,

        ROUND(
            COALESCE(rms, 0) + COALESCE(gap, 0),
            3
        ) AS reliability_error_score

    FROM cleaned_earthquake_data

    WHERE rms IS NOT NULL
      AND gap IS NOT NULL

    ORDER BY reliability_error_score DESC

    LIMIT 20;
    """

    return run_query(engine, query)

df_low_reliability = get_lowest_data_reliability(engine)

display_result(
    "28. EVENTS WITH LOWEST DATA RELIABILITY",
    df_low_reliability
)

# ============================================================
# 29. CONSECUTIVE EARTHQUAKES
#     WITHIN 50 KM AND WITHIN 1 HOUR
# ============================================================

def get_consecutive_earthquake_pairs(engine):
    """
    Find consecutive earthquakes by time that occurred
    within 50 km of each other and within 1 hour.
    """

    query = """
    WITH consecutive_events AS (
        SELECT
            id,
            time,
            latitude,
            longitude,
            mag,

            LAG(id) OVER (ORDER BY time) AS previous_id,
            LAG(time) OVER (ORDER BY time) AS previous_time,
            LAG(latitude) OVER (ORDER BY time) AS previous_latitude,
            LAG(longitude) OVER (ORDER BY time) AS previous_longitude,
            LAG(mag) OVER (ORDER BY time) AS previous_mag

        FROM cleaned_earthquake_data

        WHERE time IS NOT NULL
          AND latitude IS NOT NULL
          AND longitude IS NOT NULL
    )

    SELECT
        previous_id,
        id,

        previous_time,
        time,

        previous_latitude,
        previous_longitude,

        latitude,
        longitude,

        previous_mag,
        mag,

        ROUND(
            TIMESTAMPDIFF(
                SECOND,
                previous_time,
                time
            ) / 3600,
            2
        ) AS time_difference_hours,

        ROUND(
            6371 * 2 * ASIN(
                SQRT(
                    POWER(
                        SIN(
                            RADIANS(
                                latitude - previous_latitude
                            ) / 2
                        ),
                        2
                    )
                    +
                    COS(
                        RADIANS(previous_latitude)
                    )
                    *
                    COS(
                        RADIANS(latitude)
                    )
                    *
                    POWER(
                        SIN(
                            RADIANS(
                                longitude - previous_longitude
                            ) / 2
                        ),
                        2
                    )
                )
            ),
            2
        ) AS distance_km

    FROM consecutive_events

    WHERE previous_time IS NOT NULL

      AND TIMESTAMPDIFF(
            SECOND,
            previous_time,
            time
          ) <= 3600

      AND
          6371 * 2 * ASIN(
              SQRT(
                  POWER(
                      SIN(
                          RADIANS(
                              latitude - previous_latitude
                          ) / 2
                      ),
                      2
                  )
                  +
                  COS(
                      RADIANS(previous_latitude)
                  )
                  *
                  COS(
                      RADIANS(latitude)
                  )
                  *
                  POWER(
                      SIN(
                          RADIANS(
                              longitude - previous_longitude
                          ) / 2
                      ),
                      2
                  )
              )
          ) <= 50

    ORDER BY time;
    """

    return run_query(engine, query)

df_consecutive_pairs = get_consecutive_earthquake_pairs(engine)

display_result(
    "29. CONSECUTIVE EARTHQUAKES WITHIN 50 KM AND 1 HOUR",
    df_consecutive_pairs
)
# ============================================================
# 30. REGIONS WITH MOST DEEP-FOCUS EARTHQUAKES
#     DEPTH > 300 KM
# ============================================================

def get_deep_focus_regions(engine):
    """
    Get countries with the highest frequency of
    deep-focus earthquakes (depth > 300 km).
    """

    query = """
    SELECT
        country,
        COUNT(*) AS deep_earthquake_count

    FROM cleaned_earthquake_data

    WHERE depth_km > 300
      AND country IS NOT NULL
      AND country <> 'Unknown'

    GROUP BY country

    ORDER BY deep_earthquake_count DESC;
    """

    return run_query(engine, query)

df_deep_regions = get_deep_focus_regions(engine)

display_result(
    "30. REGIONS WITH HIGHEST FREQUENCY OF DEEP-FOCUS EARTHQUAKES",
    df_deep_regions
)

# ============================================================
# END
# ============================================================

print("\n" + "=" * 70)
print("SQL ANALYSIS TASKS COMPLETED SUCCESSFULLY")
print("=" * 70)


sys.stdout = sys.__stdout__
output_file.close()

print("Data analysis completed using SQL.")
print("Output saved to sql_analysis_output.txt")