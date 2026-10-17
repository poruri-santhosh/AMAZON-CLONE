
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import matplotlib.pyplot as plt
from data_loader import load_data

df = load_data()
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IMAGE_DIR = os.path.join(PROJECT_ROOT, "reports", "visualisations")
os.makedirs(IMAGE_DIR, exist_ok=True)

views = df["total_views"]

Q1 = views.quantile(0.25)
median = views.median()
Q3 = views.quantile(0.75)
IQR = Q3 - Q1

print("Minimum:", views.min())
print("Q1:", Q1)
print("Median:", median)
print("Q3:", Q3)
print("Maximum:", views.max())
print("IQR:", IQR)

print("Lower outlier boundary:", Q1 - 1.5 * IQR)
print("Upper outlier boundary:", Q3 + 1.5 * IQR)

print("*"*100)

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = views[(views < lower) | (views > upper)]

print("Total products:", len(views))
print("Number of outliers:", len(outliers))
print("Outlier values:")
print(outliers.value_counts().sort_index())

outlier_rows = df.loc[
    (views < lower) | (views > upper)
]

print("\nOutlier products:")
print(outlier_rows.to_string(index=False))


print("*"*100)
plt.figure(figsize=(10, 5))

plt.boxplot(df["total_views"], orientation="horizontal")

plt.title("Box Plot of Product Views")
plt.xlabel("Total Views")

plt.tight_layout()
output_path = os.path.join(IMAGE_DIR, "product_views_boxplot.png")
plt.savefig(output_path, dpi=160, bbox_inches="tight")
plt.close()
print(f"Visualization saved to: {output_path}")
