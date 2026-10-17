# ====================================================================
# STEP 1: LIBRARIES IMPORT & DATA LOADING
# ====================================================================
import os

import pandas as pd
import numpy as np

# CSV file load chestunnam
file_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "raw",
    "product_views_analysis.csv",
)
df = pd.read_csv(file_path)

print("=" * 60)
print("STEP 1: DATA LOAD AYINDI - FIRST 5 ROWS:")
print("=" * 60)
print(df.head())


# ====================================================================
# STEP 2: BASIC SHAPE & STRUCTURE CHECK
# ====================================================================
print("\n" + "=" * 60)
print("STEP 2: DATASET SHAPE & COLUMN TYPES:")
print("=" * 60)
print(f"Total Rows (Records): {df.shape[0]}")
print(f"Total Columns: {df.shape[1]}")
print("\nColumn Data Types:")
print(df.dtypes)


# ====================================================================
# STEP 3: MISSING / NULL VALUES CHECK
# ====================================================================
print("\n" + "=" * 60)
print("STEP 3: MISSING VALUES (NULLS) CHECK:")
print("=" * 60)
null_counts = df.isnull().sum()
null_percent = (df.isnull().sum() / len(df)) * 100

null_summary = pd.DataFrame({
    'Missing_Count': null_counts,
    'Missing_Percentage (%)': null_percent
})
print(null_summary)


# ====================================================================
# STEP 4: DUPLICATE VALUES CHECK
# ====================================================================
print("\n" + "=" * 60)
print("STEP 4: DUPLICATE CHECK:")
print("=" * 60)
total_duplicates = df.duplicated().sum()
asin_duplicates = df['asin'].duplicated().sum()

print(f"Entire Row Duplicates: {total_duplicates}")
print(f"Duplicate ASINs (Primary Key check): {asin_duplicates}")


# ====================================================================
# STEP 5: NUMERICAL STATISTICAL SUMMARY (OUTLIERS & DISTRIBUTION)
# ====================================================================
print("\n" + "=" * 60)
print("STEP 5: STATISTICAL SUMMARY (describe):")
print("=" * 60)
print(df.describe().round(2))


# ====================================================================
# STEP 6: BUSINESS LOGIC & DATA QUALITY AUDIT REPORT
# ====================================================================
print("\n" + "=" * 60)
print("STEP 6: DATA QUALITY FINDINGS & WARNINGS:")
print("=" * 60)

# Check 1: total_views zero unnaya leda check cheyadam
zero_views_count = (df['total_views'] == 0).sum()
if zero_views_count > 0:
    print(f"[CRITICAL WARNING] {zero_views_count} products ki 'total_views' 0 ga undi!")
    print("-> Reason: Database views table nunchi aggregate avvaledu leda JOIN match kaledu.")

# Check 2: Invalid price check (Price <= 0)
invalid_prices = (df['standard_price'] <= 0).sum()
print(f"[INFO] Invalid/Zero Prices Count: {invalid_prices}")

# Check 3: Invalid rating check (Rating < 1 or Rating > 5)
invalid_ratings = (~df['average_rating'].between(1.0, 5.0)).sum()
print(f"[INFO] Out-of-range Ratings Count: {invalid_ratings}")

print("\nData Understanding & Quality Assessment complete ayindi mowa!")
print(df["standard_price"].isnull().sum())