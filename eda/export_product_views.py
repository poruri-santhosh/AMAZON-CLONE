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
    COUNT(v.view_id) AS total_views,
    ROUND(AVG(p.rating)::numeric, 2) AS average_rating,
    p.standard_price
FROM catalog.dim_products AS p
LEFT JOIN retail_traffic.fact_glance_views AS v
    ON p.asin = v.asin
GROUP BY
    p.asin,
    p.product_title,
    p.rating,
    p.standard_price
ORDER BY total_views DESC;
"""

output_path = PROJECT_ROOT / "data" / "raw" / "product_views_analysis.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

with create_engine(database_url).connect() as connection:
    df = pd.read_sql_query(query, connection)

df.to_csv(output_path, index=False)

print(f"Export complete: {output_path}")
print(df.head())
