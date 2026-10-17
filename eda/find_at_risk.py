import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
import pandas as pd
from data_loader import load_data

df = load_data()


# 1. Apply segmentation logic
def assign_segment(row):
    high_views = row["total_views"] >= 20
    high_rating = row["average_rating"] >= 4.2

    if high_views and high_rating:
        return "Stars (High Traffic, High Rating)"
    elif not high_views and high_rating:
        return "Hidden Gems (Low Traffic, High Rating)"
    elif high_views and not high_rating:
        return "At Risk (High Traffic, Low Rating)"
    else:
        return "Dead Weight (Low Traffic, Low Rating)"


df["segment"] = df.apply(assign_segment, axis=1)

# 2. Filter At Risk products
at_risk_products = df[df["segment"] == "At Risk (High Traffic, Low Rating)"].sort_values(
    by="total_views", ascending=False
)

print("=" * 65)
print(f"TOTAL AT RISK PRODUCTS FOUND: {len(at_risk_products)}")
print("=" * 65)
print(
    at_risk_products[
        [
            "asin",
            "product_title",
            "average_rating",
            "standard_price",
            "total_views",
        ]
    ].to_string(index=False)
)