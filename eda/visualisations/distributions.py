import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib.pyplot as plt
from data_loader import load_data


df = load_data()
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IMAGE_DIR = os.path.join(PROJECT_ROOT, "reports", "visualisations")
os.makedirs(IMAGE_DIR, exist_ok=True)

# # Full distribution
# plt.figure(figsize=(10, 5))
# plt.hist(df["total_views"], bins=20, edgecolor="black")
# plt.title("Distribution of Product Views — All Products")
# plt.xlabel("Total Views")
# plt.ylabel("Number of Products")
# plt.tight_layout()
# plt.show()

# Zoom in on products with 0–100 views
plt.figure(figsize=(10, 5))
plt.hist(df["total_views"], bins=range(0, 111, 10), edgecolor="black")
plt.title("Distribution of Product Views — 0 to 100 Views")
plt.xlabel("Total Views")
plt.ylabel("Number of Products")
plt.xticks(range(0, 101, 10))
plt.tight_layout()
output_path = os.path.join(IMAGE_DIR, "product_views_distribution.png")
plt.savefig(output_path, dpi=160, bbox_inches="tight")
plt.close()
print(f"Visualization saved to: {output_path}")
