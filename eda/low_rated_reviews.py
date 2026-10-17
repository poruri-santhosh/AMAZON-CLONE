from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
csv_path = PROJECT_ROOT / "data" / "processed" / "at_risk_products_reviews.csv"

df_rev = pd.read_csv(csv_path)

print("=" * 60)
print("1. INDIVIDUAL REVIEW RATING BREAKDOWN (for Low-Rated Catalog):")
print(df_rev["individual_review_rating"].value_counts().sort_index())

print("\n" * 1 + "=" * 60)
print("2. PRODUCTS WITH MOST NEGATIVE REVIEWS:")
summary = (
    df_rev.groupby(["asin", "product_title", "overall_product_rating"])
    .agg(
        total_reviews=("review_id", "count"),
        avg_user_rating=("individual_review_rating", "mean"),
    )
    .reset_index()
    .sort_values(by=["overall_product_rating", "total_reviews"], ascending=[True, False])
)

print(summary.head(10).to_string(index=False))