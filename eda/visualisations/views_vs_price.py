
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

fig, ax = plt.subplots(figsize=(10, 5))

ax.scatter(
    df["standard_price"],
    df["total_views"]
)

ax.set_title("Product Price vs Total Views")
ax.set_xlabel("Standard Price")
ax.set_ylabel("Total Views")

fig.tight_layout()
output_path = os.path.join(IMAGE_DIR, "product_price_vs_views.png")
fig.savefig(output_path, dpi=160, bbox_inches="tight")
plt.close(fig)
print(f"Visualization saved to: {output_path}")
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from data_loader import load_data

df = load_data()

# Calculate Pearson Correlation
correlation = df["standard_price"].corr(df["total_views"])
print(f"Correlation between Price and Views: {correlation:.4f}")