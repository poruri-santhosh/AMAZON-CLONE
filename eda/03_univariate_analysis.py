
from data_loader import load_data

df = load_data()

# 1. Analyze product views
print("\n--- PRODUCT VIEWS ---")
print(df["total_views"].describe())

# 2. Analyze ratings
print("\n--- PRODUCT RATINGS ---")
print(df["average_rating"].describe())

# 3. Analyze prices
print("\n--- PRODUCT PRICES ---")
print(df["standard_price"].describe())

# 4. Count products in rating groups
print("\n--- RATING DISTRIBUTION ---")
print(
    df["average_rating"]
    .value_counts(bins=5)
    .sort_index()
)

print("\nUnivariate analysis complete!")
