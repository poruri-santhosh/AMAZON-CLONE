
from data_loader import load_data

# Load the dataset using our existing loader
df = load_data()

# 1. Dataset dimensions
print("\n--- DATASET SIZE ---")
print("Rows and columns:", df.shape)

# 2. Column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

# 3. Data types and non-null counts
print("\n--- DATASET INFORMATION ---")
df.info()

# 4. Statistical summary
print("\n--- NUMERICAL SUMMARY ---")
print(df.describe())

# 5. Sample records
print("\n--- SAMPLE DATA ---")
print(df.head())
