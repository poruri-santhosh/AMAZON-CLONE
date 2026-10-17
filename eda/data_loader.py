
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "product_views_analysis.csv"


def load_data():
    """Load the product views dataset."""
    df = pd.read_csv(DATA_PATH)
    return df


if __name__ == "__main__":
    df = load_data()

    print("Dataset loaded successfully!")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(df.head())
