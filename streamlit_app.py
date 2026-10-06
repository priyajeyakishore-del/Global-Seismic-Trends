import streamlit as st

from import_csv_sql import engine

from data_analysis import *
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Global Seismic Trends",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🌍 Global Seismic Trends")

st.caption(
    "Data-Driven Earthquake Insights for Disaster Management"
)

st.write(
    "🌎 **Global Coverage**  |  "
    "📅 **2021 – 2026**  |  "
    "🗄️ **USGS Earthquake Data**  |  "
    "💻 **Python • MySQL • Streamlit**"
)

st.divider()


# ============================================================
# EARTHQUAKE OVERVIEW
# ============================================================

st.subheader("📊 Earthquake Overview")


# Get total earthquakes
df_total = get_total_earthquakes(engine)

total_earthquakes = int(
    df_total.iloc[0]["total_earthquakes"]
)


# Get strongest earthquake
df_strongest = get_top_10_strongest_earthquakes(engine)

strongest_magnitude = df_strongest.iloc[0]["mag"]


# Get deepest earthquake
df_deepest = get_top_10_deepest_earthquakes(engine)

deepest_depth = df_deepest.iloc[0]["depth_km"]

# get total tsunamis
df_tsunamis = get_total_tsunamis(engine)
total_tsunamis = int(df_tsunamis.iloc[0]["total_tsunamis"])

# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌍 Total Earthquakes",
        f"{total_earthquakes:,}"
    )

with col2:
    st.metric(
        "💥 Strongest Magnitude",
        f"{strongest_magnitude:.1f}"
    )

with col3:
    st.metric(
        "🌊 Deepest Earthquake",
        f"{deepest_depth:.2f} km"
    )

with col4:
    st.metric(
        "🌊 Total Tsunami Events",
        f"{total_tsunamis:,}"
    )


st.divider()

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview",
    "📈 Time Trends",
    "🌎 Geographic Analysis",
    "💥 Magnitude & Depth",
    "🌊 Tsunami & Alerts",
    "📡 Data Quality",
    "📊 Visualizations"
])
# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab1:

    st.subheader("📊 Earthquake Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.write("### 💥 Top 10 Strongest Earthquakes")

        df = get_top_10_strongest_earthquakes(engine)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    with col2:

        st.write("### 🌊 Top 10 Deepest Earthquakes")

        df = get_top_10_deepest_earthquakes(engine)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    st.write("### 🚨 Shallow & Strong Earthquakes")

    df = get_shallow_strong_earthquakes(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    st.write("### 🌎 Average Magnitude by Magnitude Type")

    df = get_average_magnitude_per_mag_type(engine)

    st.bar_chart(
        df.set_index("magType")["average_magnitude"]
    )

# ============================================================
# TAB 2 — TIME TRENDS
# ============================================================

with tab2:

    st.subheader("📈 Earthquake Time Trends")

    col1, col2 = st.columns(2)

    with col1:

        st.write("### 📅 Year with Most Earthquakes")

        df = get_year_with_most_earthquakes(engine)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    with col2:

        st.write("### 📅 Month with Most Earthquakes")

        df = get_month_with_most_earthquakes(engine)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    st.write("### 📆 Day with Most Earthquakes")

    df = get_day_with_most_earthquakes(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    st.write("### 🕐 Earthquakes by Hour")

    df_hour = get_earthquakes_per_hour(engine)

    st.write(df_hour)   # check the returned data

    st.line_chart(
    df_hour,
    x="hour_of_day",
    y="earthquake_count"
    )
    st.write("### 📈 Year-over-Year Growth")

    df = get_year_over_year_growth_rate(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    st.write("### 📈 Year-over-Year Growth Rate")

    df = get_year_over_year_growth_rate(engine)

    df["yoy_growth_rate"] = pd.to_numeric(
        df["yoy_growth_rate"],
        errors="coerce"
    )

    df["yoy_growth_rate"] = df["yoy_growth_rate"].round(2)

    df = df.dropna(subset=["yoy_growth_rate"])

    st.line_chart(
        df,
        x="year",
        y="yoy_growth_rate",
        height=300
    )

# ============================================================
# TAB 3
# GEOGRAPHIC ANALYSIS
# ============================================================

with tab3: 
    st.subheader("🌎 Geographic Analysis")
    # --------------------------------------------------------
    # Task 21
    # --------------------------------------------------------

    st.write(
        "### 🌍 Top 5 Countries by Average Magnitude"
    )

    df = get_top_5_countries_by_avg_magnitude(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------------
    # Task 22
    # --------------------------------------------------------

    st.write(
        "### 🌎 Countries with Shallow & Deep "
        "Earthquakes in Same Month"
    )

    df = get_countries_with_shallow_deep_same_month(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------------
    # Task 24
    # --------------------------------------------------------

    st.write(
        "### 🌎 Top 3 Seismically Active Regions"
    )

    df = get_top_3_active_regions(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
        # --------------------------------------------------------
    # Task 25
    # --------------------------------------------------------

    st.write(
        "### 🌐 Average Depth Near Equator"
    )

    df = get_average_depth_near_equator(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------------
    # Task 30
    # --------------------------------------------------------

    st.write(
        "### 📍 Deep-Focus Earthquakes by Region"
    )

    df = get_deep_focus_regions(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
# ============================================================
# TAB 4
# MAGNITUDE & DEPTH
# ============================================================

with tab4:

    st.subheader("💥 Magnitude & Depth Analysis")

    # --------------------------------------------------------
    # Task 5
    # --------------------------------------------------------

    st.write(
        "### 📊 Average Magnitude per Magnitude Type"
    )

    col1, col2 = st.columns(2)

    df = get_average_magnitude_per_mag_type(engine)

    with col1:
        st.write("### 📋 Result ")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("### 📊 Bar Chart")
        st.bar_chart(
            df,
            x="magType",
            y="average_magnitude",
            height=500
        )
    # --------------------------------------------------------
    # Task 18
    # --------------------------------------------------------

    st.write(
        "### 📡 High Station Coverage"
    )

    df, station_threshold = get_high_station_coverage(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------------
    # Task 26
    # --------------------------------------------------------

    st.write(
        "### 📏 Highest Shallow/Deep Ratio"
    )

    df = get_highest_shallow_deep_ratio(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Task 27
    # --------------------------------------------------------

    st.write(
        "### 🌊 Tsunami vs Non-Tsunami "
        "Magnitude Comparison"
    )

    df = get_average_magnitude_tsunami_difference(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------------
    # Strongest / Deepest summary
    # --------------------------------------------------------

    st.write("### 🔎 Extreme Earthquake Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "💥 Maximum Magnitude",
            f"{strongest_magnitude:.1f}"
        )

    with col2:

        st.metric(
            "📏 Maximum Depth",
            f"{deepest_depth:.2f} km"
        )
#============================================================
# TAB 5
# TSUNAMI & ALERTS
# ============================================================

with tab5:

    st.subheader("🌊 Tsunami & Alert Analysis")


    # --------------------------------------------------------
    # Task 19
    # --------------------------------------------------------

    st.write("### 🌊 Tsunamis per Year")

    df = get_tsunamis_per_year(engine)

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📋 Tsunami Data")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("#### 📊 Tsunami Trend")

        st.bar_chart(
            df.set_index("year")["tsunami_count"],
            height=300
        )


    # --------------------------------------------------------
    # Task 20
    # --------------------------------------------------------

    st.write("### 🚨 Task 20 — Earthquakes by Alert Level")

    df = get_earthquakes_by_alert_level(engine)

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📋 Alert Level Data")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("#### 📊 Earthquakes by Alert Level")

        st.bar_chart(
            df.set_index("alert")["earthquake_count"],
            height=300
        )
    # --------------------------------------------------------
    # Task 14
    # --------------------------------------------------------

    st.write("### 📊 Reviewed vs Automatic")

    df = get_reviewed_vs_automatic(engine)

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📋 Status Data")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("#### 📊 Reviewed vs Automatic")

        st.bar_chart(
            df.set_index("status")["earthquake_count"],
            height=300
        )

    # --------------------------------------------------------
    # Task 15
    # --------------------------------------------------------

    st.write("### 🌐 Earthquakes by Type")

    df = get_count_by_earthquake_type(engine)

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📋 Earthquake Type Data")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("#### 📊 Earthquakes by Type")

        fig = px.bar(
            df,
            x="earthquake_count",
            y="type",
            orientation="h",
            title="Earthquakes by Type"
        )

        fig.update_layout(
            xaxis_title="Earthquake Count",
            yaxis_title="Earthquake Type",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    # --------------------------------------------------------
    # Task 16
    # --------------------------------------------------------

    st.write("### 📋 Earthquakes by Data Type")

    df = get_count_by_data_type(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 6
# DATA QUALITY & ADVANCED INSIGHTS
# ============================================================

with tab6:

    st.subheader("📡 Data Quality & Advanced Insights")

    # --------------------------------------------------------
    # Task 10
    # --------------------------------------------------------

    st.write("### 📡 Most Active Reporting Network")

    df = get_most_active_reporting_network(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------------
    # Task 28
    # --------------------------------------------------------

    st.write(
        "### ⚠️ Lowest Data Reliability Events"
    )

    df = get_lowest_data_reliability(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------------
    # Task 18
    # --------------------------------------------------------

    st.write(
        "### 📡 High Station Coverage Events"
    )

    df, station_threshold = get_high_station_coverage(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    # --------------------------------------------------------
    # Task 30
    # --------------------------------------------------------

    st.write(
        "### 🌎 Deep-Focus Earthquakes"
    )

    df = get_deep_focus_regions(engine)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    st.write("### 📊 Data Quality Summary")

    st.write(
        "This section focuses on reporting networks, "
        "station coverage, reliability indicators, "
        "and deep-focus earthquake patterns."
    )
# ============================================================
# TAB 7 — VISUALIZATIONS
# ============================================================

with tab7:

    st.subheader("📊 Earthquake Visualizations")

    st.caption(
        "Key visual insights from the cleaned USGS earthquake dataset."
    )

    st.write("##### 🌍 Total Earthquake Events")

    total_query = """
        SELECT COUNT(*) AS total_events
        FROM cleaned_earthquake_data
        """

    df_total = __import__("data_analysis").run_query(
            engine,
            total_query
        )

    total_events = df_total["total_events"].iloc[0]

    st.metric(
            "🌍 Total Earthquake Events",
            f"{total_events:,}"
        )

    st.caption(
            "Over 137,000 earthquakes were recorded, providing a robust dataset for global seismic analysis."
        )
    col1, col2= st.columns(2)
    with col1:

        st.write("### 📈 Magnitude Distribution")

        magnitude_query = """
        SELECT mag
        FROM cleaned_earthquake_data
        WHERE mag IS NOT NULL
        """

        df_magnitude = __import__(
            "data_analysis"
        ).run_query(
            engine,
            magnitude_query
        )

        fig_mag = px.histogram(
            df_magnitude,
            x="mag",
            nbins=30,
            title="Earthquake Magnitude Distribution",
            labels={
                "mag": "Magnitude",
                "count": "Number of Earthquakes"
            }
        )

        fig_mag.add_vline(
            x=7.5,
            line_dash="dash",
            annotation_text="Megaquake > 7.5"
        )

        fig_mag.update_layout(
            height=300
        )

        st.plotly_chart(
            fig_mag,
            use_container_width=True
        )
        st.info("The histogram illustrates the Earthquake Magnitude Distribution from the USGS dataset." \
                   "Most recorded earthquakes fall between magnitude 3.0 and 5.0, " \
                   "with the highest frequency around magnitude 4, exceeding 40,000 events. " \
                   "The dashed line at 7.5 marks the threshold for megaquakes, " \
                   "emphasizing that extremely powerful earthquakes are rare compared to moderate ones.")
    with col2:
        st.write("### 📏 Earthquake Depth Distribution")
        depth_category_query = """
        SELECT
            depth_category,
            COUNT(*) AS earthquake_count
        FROM cleaned_earthquake_data
        WHERE depth_category IS NOT NULL
        GROUP BY depth_category
        ORDER BY earthquake_count DESC
        """

        df_depth_category = __import__(
            "data_analysis"
        ).run_query(
            engine,
            depth_category_query
        )

        fig_depth_category = px.bar(
            df_depth_category,
            x="depth_category",
            y="earthquake_count",
            title="Earthquakes by Depth Category",
            labels={
                "depth_category": "Depth Category",
                "earthquake_count": "Number of Earthquakes"
            },
            text="earthquake_count"
        )

        fig_depth_category.update_layout(
            height=300
        )

        st.plotly_chart(
            fig_depth_category,
            use_container_width=True
        )
        st.info("This visualization highlights that most seismic events occur near the Earth’s surface, " \
                   "where they tend to cause greater damage and are more frequently recorded.")
    # ============================================================
    # GRAPH — EARTHQUAKE SEASONALITY
    # ============================================================

    st.write("### 📅 Earthquake Seasonality")

    seasonality_query = """
    SELECT
        month,
        month_name,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE month IS NOT NULL
    GROUP BY month, month_name
    ORDER BY month
    """

    df_seasonality = __import__("data_analysis").run_query(
            engine,
            seasonality_query
        )

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📋 Monthly Earthquake Data")

        st.dataframe(
            df_seasonality,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("#### 📊 Monthly Earthquake Activity")

        fig_seasonality = px.bar(
        df_seasonality,
        x="month_name",
        y="earthquake_count",
        title="Earthquake Activity by Month",
        labels={
            "month_name": "Month",
            "earthquake_count": "Number of Earthquakes"
            },
            text="earthquake_count"
        )

        fig_seasonality.update_layout(
            xaxis_title="Month",
            yaxis_title="Number of Earthquakes",
            height=300
            )

        st.plotly_chart(
            fig_seasonality,
            use_container_width=True
            )
        st.info(
        "📌 Seasonality Insight: Some months may show slightly higher "
        "earthquake activity, but the overall pattern does not indicate "
        "that earthquakes are strictly seasonal."
        )
    # ============================================================
    # GEOGRAPHIC INSIGHTS
    # ============================================================

    st.write("## 🌐 Geographic Insights")


    # ------------------------------------------------------------
    # 1. TOP COUNTRIES BY MAGNITUDE
    # ------------------------------------------------------------

    st.write("### 🌋 Top Countries by Maximum Magnitude")

    top_magnitude_query = """
    SELECT
        country,
        MAX(mag) AS maximum_magnitude,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE country IS NOT NULL
    AND country <> 'Unknown'
    AND mag IS NOT NULL
    GROUP BY country
    ORDER BY maximum_magnitude DESC
    LIMIT 10
    """

    df_top_magnitude = __import__("data_analysis").run_query(
        engine,
        top_magnitude_query
    )

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📋 Data")
        st.dataframe(
            df_top_magnitude,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("#### 📊 Maximum Magnitude")

        fig_magnitude_country = px.bar(
            df_top_magnitude,
            x="maximum_magnitude",
            y="country",
            orientation="h",
            title="Top Countries by Maximum Earthquake Magnitude",
            labels={
                "country": "Country",
                "maximum_magnitude": "Maximum Magnitude"
            }
        )

        fig_magnitude_country.update_layout(
            height=400
        )

        st.plotly_chart(
            fig_magnitude_country,
            use_container_width=True
        )
    # ------------------------------------------------------------
    # 2. EQUATORIAL ZONE
    # ------------------------------------------------------------

    st.write("### 🌍 Equatorial Zone — ±5° Latitude")

    df_equator = get_average_depth_near_equator(engine)

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📋 Equatorial Earthquake Data")

        st.dataframe(
            df_equator.head(),
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("#### 📊 Average Depth")

        fig_equator = px.bar(
            df_equator.head(),
            x="average_depth_km",
            y="country",
            orientation="h",
            title="Average Earthquake Depth Near the Equator",
            labels={
                "country": "Country",
                "average_depth_km": "Average Depth (km)"
            }
        )

        fig_equator.update_layout(
            height=300
        )

        st.plotly_chart(
            fig_equator,
            use_container_width=True
        )
    # ------------------------------------------------------------
    # 3. SEISMICALLY ACTIVE REGIONS
    # ------------------------------------------------------------

    st.write("### 🔥 Seismically Active Regions")

    active_regions_query = """
    SELECT
        country,
        COUNT(*) AS earthquake_count,
        ROUND(AVG(mag), 2) AS average_magnitude
    FROM cleaned_earthquake_data
    WHERE country IS NOT NULL
    AND country <> 'Unknown'
    AND mag IS NOT NULL
    GROUP BY country
    HAVING COUNT(*) >= 50
    ORDER BY earthquake_count DESC
    """

    df_active_regions = __import__("data_analysis").run_query(
        engine,
        active_regions_query
    )

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📋 Frequency + Magnitude")

        st.dataframe(
            df_active_regions,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("#### 📊 Frequency vs Average Magnitude")

        fig_active = px.scatter(
            df_active_regions,
            x="earthquake_count",
            y="average_magnitude",
            hover_name="country",
            title="Seismic Activity by Country",
            labels={
                "earthquake_count": "Number of Earthquakes",
                "average_magnitude": "Average Magnitude"
            }
        )

        fig_active.update_layout(
            height=300
        )

        st.plotly_chart(
            fig_active,
            use_container_width=True
        )
    st.info(
    "🌐 Geographic Insight: Earthquake activity is concentrated in "
    "specific tectonically active regions. Countries around the "
    "Pacific Ring of Fire generally show high earthquake frequency "
    "and significant magnitudes. Equatorial regions also display "
    "distinct depth patterns."
    )
    # ============================================================
    # 🌊 TSUNAMI & ALERTS
    # ============================================================

    st.write("## 🌊 Tsunami & Alerts")


    # ------------------------------------------------------------
    # 1. TSUNAMI VS NON-TSUNAMI
    # ------------------------------------------------------------

    st.write("### 🌊 Tsunami-Generating Earthquakes")

    tsunami_query = """
    SELECT
        CASE
            WHEN tsunami = 1 THEN 'Tsunami'
            ELSE 'Non-Tsunami'
        END AS tsunami_status,
        COUNT(*) AS earthquake_count
    FROM cleaned_earthquake_data
    WHERE tsunami IS NOT NULL
    GROUP BY tsunami
    ORDER BY earthquake_count DESC
    """

    df_tsunami = __import__("data_analysis").run_query(
        engine,
        tsunami_query
    )

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📋 Tsunami Data")

        st.dataframe(
            df_tsunami,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("#### 📊 Tsunami vs Non-Tsunami")

        fig_tsunami = px.bar(
            df_tsunami,
            x="tsunami_status",
            y="earthquake_count",
            title="Tsunami vs Non-Tsunami Earthquakes",
            labels={
                "tsunami_status": "Event Type",
                "earthquake_count": "Number of Earthquakes"
            },
            text="earthquake_count"
        )

        fig_tsunami.update_layout(
            height=300
        )

        st.plotly_chart(
            fig_tsunami,
            use_container_width=True
        )


    # ------------------------------------------------------------
    # 2. ALERT LEVELS
    # ------------------------------------------------------------

    st.write("### 🚨 Earthquake Alert Levels")

    alert_query = """
    SELECT
        alert_level,
        COUNT(*) AS earthquake_count
    FROM (
        SELECT
            LOWER(TRIM(alert)) AS alert_level
        FROM cleaned_earthquake_data
        WHERE alert IS NOT NULL
        AND TRIM(alert) <> ''
    ) AS alert_data
    GROUP BY alert_level
    ORDER BY
        CASE
            WHEN alert_level = 'red' THEN 1
            WHEN alert_level = 'orange' THEN 2
            WHEN alert_level = 'yellow' THEN 3
            WHEN alert_level = 'green' THEN 4
            ELSE 5
        END
    """

    df_alert = __import__("data_analysis").run_query(
        engine,
        alert_query
    )

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📋 Alert-Level Data")

        st.dataframe(
            df_alert,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.write("#### 📊 Alert Level Distribution")

        fig_alert = px.bar(
            df_alert,
            x="alert_level",
            y="earthquake_count",
            title="Earthquake Alert Levels",
            labels={
                "alert_level": "Alert Level",
                "earthquake_count": "Number of Earthquakes"
            },
            text="earthquake_count"
        )

        fig_alert.update_layout(
            height=300
        )

        st.plotly_chart(
            fig_alert,
            use_container_width=True
        )
    st.info(
        "🌊 Tsunami Insight: Only a small proportion of recorded "
        "earthquakes are associated with tsunami indicators. "
        "Alert levels are concentrated in the lower categories, "
        "while higher alert levels represent relatively rare and "
        "potentially more significant events."
    )
    # ============================================================
    # 📊 DATA QUALITY — DEPTH OUTLIERS
    # ============================================================

    st.write("## 📊 Data Quality & Reliability")

    st.write("### ⚠️ Depth Outliers")

    st.caption(
        "Depth outliers are identified using the IQR statistical method. "
        "A statistical outlier is not necessarily a data error."
    )


    # ============================================================
    # 1. IQR LIMITS
    # ============================================================

    LOWER_LIMIT = -63.38
    UPPER_LIMIT = 132.30


    # ============================================================
    # 2. TOTAL DEPTH RECORDS
    # ============================================================

    total_query = """
    SELECT
        COUNT(*) AS total_depth_records
    FROM cleaned_earthquake_data
    WHERE depth_km IS NOT NULL
    """

    df_total = __import__("data_analysis").run_query(
        engine,
        total_query
    )

    total_depth_records = int(
        df_total["total_depth_records"].iloc[0]
    )


    # ============================================================
    # 3. COUNT DEPTH OUTLIERS
    # ============================================================

    outlier_count_query = f"""
    SELECT
        COUNT(*) AS outlier_events
    FROM cleaned_earthquake_data
    WHERE depth_km IS NOT NULL
    AND (
            depth_km < {LOWER_LIMIT}
            OR depth_km > {UPPER_LIMIT}
        )
    """

    df_outlier_count = __import__("data_analysis").run_query(
        engine,
        outlier_count_query
    )

    outlier_events = int(
        df_outlier_count["outlier_events"].iloc[0]
    )


    # ============================================================
    # 4. CALCULATE OUTLIER PERCENTAGE
    # ============================================================

    if total_depth_records > 0:

        outlier_percentage = (
            outlier_events / total_depth_records
        ) * 100

    else:

        outlier_percentage = 0


    # ============================================================
    # 5. DISPLAY METRICS
    # ============================================================

    metric1, metric2, metric3 = st.columns(3)

    with metric1:

        st.metric(
            "Total Depth Records",
            f"{total_depth_records:,}"
        )

    with metric2:

        st.metric(
            "Depth Outliers",
            f"{outlier_events:,}"
        )

    with metric3:

        st.metric(
            "Outlier Percentage",
            f"{outlier_percentage:.2f}%"
        )


    # ============================================================
    # 6. GET OUTLIER EVENTS
    # ============================================================

    outlier_query = f"""
    SELECT
        id,
        country,
        place,
        depth_km,
        depth_category,
        mag
    FROM cleaned_earthquake_data
    WHERE depth_km IS NOT NULL
    AND (
            depth_km < {LOWER_LIMIT}
            OR depth_km > {UPPER_LIMIT}
        )
    ORDER BY depth_km DESC
    """

    df_depth_outliers = __import__("data_analysis").run_query(
        engine,
        outlier_query
    )


    # ============================================================
    # 7. DATA + GRAPH
    # ============================================================

    col1, col2 = st.columns(2)


    # ------------------------------------------------------------
    # LEFT — OUTLIER DATA
    # ------------------------------------------------------------

    with col1:

        st.write("#### 📋 Depth Outlier Events")

        st.dataframe(
            df_depth_outliers,
            use_container_width=True,
            hide_index=True
        )


    # ------------------------------------------------------------
    # RIGHT — OUTLIER GRAPH
    # ------------------------------------------------------------

    with col2:

        st.write("#### 📊 Depth Outliers vs Magnitude")

        fig_depth_outliers = px.scatter(
            df_depth_outliers,
            x="depth_km",
            y="mag",
            hover_name="place",
            title="Depth Outliers vs Magnitude",
            labels={
                "depth_km": "Depth (km)",
                "mag": "Magnitude"
            }
        )

        # IQR lower limit
        fig_depth_outliers.add_vline(
            x=LOWER_LIMIT,
            line_dash="dash",
            annotation_text="Lower IQR Limit"
        )

        # IQR upper limit
        fig_depth_outliers.add_vline(
            x=UPPER_LIMIT,
            line_dash="dash",
            annotation_text="Upper IQR Limit"
        )

        fig_depth_outliers.update_layout(
            height=550
        )

        st.plotly_chart(
            fig_depth_outliers,
            use_container_width=True
        )


    # ============================================================
    # 8. OUTLIER INTERPRETATION
    # ============================================================

    st.info(
        f"📌 Outlier Insight: {outlier_events:,} earthquake depth values "
        f"({outlier_percentage:.2f}% of valid depth records) are identified "
        "as statistical outliers using the IQR method. Many of these "
        "values can represent legitimate deep-focus earthquakes rather "
        "than incorrect measurements."
    )
