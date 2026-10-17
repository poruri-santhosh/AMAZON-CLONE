import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL is not set. Add your Neon connection URL to .env.")

query = """
SELECT
    p.asin,
    p.product_title,
    p.rating AS overall_product_rating,
    p.standard_price,
    COUNT(DISTINCT v.view_id) AS total_views,
    r.review_id,
    r.rating AS individual_review_rating,
    r.review_title,
    r.review_text
FROM catalog.dim_products AS p
LEFT JOIN retail_traffic.fact_glance_views AS v
    ON p.asin = v.asin
LEFT JOIN catalog.dim_reviews AS r
    ON p.asin = r.asin
GROUP BY
    p.asin,
    p.product_title,
    p.rating,
    p.standard_price,
    r.review_id,
    r.rating,
    r.review_title,
    r.review_text
HAVING COUNT(DISTINCT v.view_id) >= 20 AND p.rating < 4.2
ORDER BY total_views DESC, overall_product_rating ASC;
"""

print("Connecting to Neon DB and extracting At-Risk Products & Customer Reviews...")
with create_engine(database_url).connect() as connection:
    df_at_risk_reviews = pd.read_sql_query(query, connection)

output_path = PROJECT_ROOT / "data" / "processed" / "at_risk_products_reviews.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)
df_at_risk_reviews.to_csv(output_path, index=False)

print(f"\n[SUCCESS] Extracted {len(df_at_risk_reviews)} rows into '{output_path}'!")
print("\n--- Top At-Risk Products & Reviews Preview ---")
print(
    df_at_risk_reviews[
        [
            "asin",
            "product_title",
            "overall_product_rating",
            "total_views",
            "review_title",
            "review_text",
        ]
    ].head()
)
