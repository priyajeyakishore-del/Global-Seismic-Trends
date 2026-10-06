import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


# ============================================================
# 1. READ CSV FILE
# ============================================================

csv_file = "cleaned_earthquake_data.csv"

df = pd.read_csv(csv_file)

print("=" * 60)
print("CSV FILE LOADED")
print("=" * 60)

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])


# ============================================================
# 2. CONVERT DATE COLUMNS
# ============================================================

df["time"] = pd.to_datetime(
    df["time"],
    errors="coerce"
)

df["updated"] = pd.to_datetime(
    df["updated"],
    errors="coerce"
)

print("\nDate columns converted successfully.")

print(df[["time", "updated"]].dtypes)


# ============================================================
# 3. MYSQL DATABASE CONNECTION
# ============================================================

password = "Dinnu@world"

engine = create_engine(
    f"mysql+pymysql://root:{quote_plus(password)}@localhost:3306/earthquake_db"
)

print("\nMySQL connection created successfully.")


# ============================================================
# 4. IMPORT DATA INTO MYSQL
# ============================================================

table_name = "cleaned_earthquake_data"

df.to_sql(
    name=table_name,
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000
)

print("\nData imported successfully!")
print("MySQL table:", table_name)


# ============================================================
# 5. VERIFY DATA IN MYSQL
# ============================================================

with engine.connect() as conn:

    result = conn.execute(
        text(f"SELECT COUNT(*) FROM {table_name}")
    )

    total_rows = result.scalar()

print("\n" + "=" * 60)
print("MYSQL VERIFICATION")
print("=" * 60)

print("Total rows in MySQL:", total_rows)


# ============================================================
# 6. DISPLAY SAMPLE DATA
# ============================================================

with engine.connect() as conn:

    result = conn.execute(
        text(f"""
        SELECT *
        FROM {table_name}
        LIMIT 5
        """)
    )

    sample_df = pd.DataFrame(
        result.fetchall(),
        columns=result.keys()
    )

print("\nFirst 5 rows from MySQL:")
print(sample_df)


# ============================================================
# 7. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("IMPORT COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"CSV rows       : {len(df)}")
print(f"MySQL rows     : {total_rows}")
print(f"MySQL database : earthquake_db")
print(f"MySQL table    : {table_name}")