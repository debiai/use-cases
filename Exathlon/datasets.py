import pandas as pd
import os

"""
Data loader script for the Exathlon dataset
"""


CSV_FOLDER_PATH = "data"


def create_dataset() -> pd.DataFrame:
    """Create a dataset with one row per timestamp."""
    benchmarks = os.listdir(CSV_FOLDER_PATH)
    df_list = []

    for benchmark in benchmarks:
        if not benchmark.endswith(".csv"):
            continue

        # Expected filename: 3_2_1000000_71.test.csv
        csv_file_path = os.path.join(CSV_FOLDER_PATH, benchmark)
        df = pd.read_csv(csv_file_path)
        df_list.append(df)

    return pd.concat(df_list, ignore_index=True)


if __name__ == "__main__":
    print(create_dataset())
