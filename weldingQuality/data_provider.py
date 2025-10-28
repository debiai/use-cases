import pandas as pd
import numpy as np
from debiai_data_provider import DebiAIProject, DataProvider


METADATA_PARQUET_FILE_PATH = "metadata/ds_meta.parquet"
UNWANTED_COLUMNS = ["sample_id", "sha256"]


class WeldingQualityMetadata(DebiAIProject):
    creation_date = "2025-03-20"
    # update_date = "2025-01-20"
    data: pd.DataFrame = None

    def __init__(self):
        super().__init__()
        self.name = "Welding quality detection challenge"
        self.get_project_parquet()

    def get_project_parquet(self):
        print("Loading data from parquet file")
        if self.data is not None:
            return self.data

        # Load all data, not just first 10 rows
        data = pd.read_parquet(METADATA_PARQUET_FILE_PATH)

        # Ensure the 'timestamp' column is of string type
        data["timestamp"] = data["timestamp"].astype(str)

        # Replaces dates 'dd/mm/yy hh:mm' to 'dd/mm/yyyy hh:mm'
        # For example, '19/03/19 10:00' to '20/03/2019 10:00'
        for i in range(len(data)):
            time = data.loc[i, "timestamp"]
            year = time.split("/")[-1].split(" ")[0]
            if len(year) == 2:
                data.loc[i, "timestamp"] = time.replace(
                    f"/{year} ", f"/20{year} "
                )  # noqa

        # Convert dates 'dd/mm/yyyy hh:mm' to 'yyyy-mm-dd hh:mm'
        # in column 'timestamp'
        data["timestamp"] = pd.to_datetime(
            data["timestamp"], format="%d/%m/%Y %H:%M"
        ).dt.strftime("%Y-%m-%d %H:%M")

        # Convert numpy types to native Python types for API serialization
        def convert_numpy_types(x):
            if isinstance(x, np.ndarray):
                # Convert numpy arrays to lists with native Python types
                return x.astype(object).tolist()
            elif isinstance(x, np.integer):
                return int(x)
            elif isinstance(x, np.floating):
                return float(x)
            elif isinstance(x, np.bool_):
                return bool(x)
            return x

        data = data.map(convert_numpy_types)

        self.data = data
        return self.data

    # Project Info
    def get_structure(self) -> dict:
        # Create the structure
        project_structure = {}

        for col in self.data.columns:
            if col in UNWANTED_COLUMNS:
                continue

            metrics = {}
            column_type = "auto"  # default type

            print(f"  Processing: {col} ({self.data[col].dtype})")

            # Determine column type based on content
            if pd.api.types.is_numeric_dtype(self.data[col]):
                column_type = "number"
                # Try to calculate numeric metrics only for numeric columns
                try:
                    metrics.update(
                        {
                            "min": float(min(self.data[col][0:10])),
                            "max": float(max(self.data[col][0:10])),
                            "mean": float(sum(self.data[col][0:10])) / 10,
                            "average": float(sum(self.data[col][0:10])) / 10,
                        }
                    )
                except (TypeError, ValueError):
                    pass
            elif pd.api.types.is_string_dtype(self.data[col]):
                column_type = "text"

            # Metrics for all column types
            try:
                metrics.update(
                    {
                        "nbUniqueValues": int(self.data[col].nunique()),
                        "nbNullValues": int(self.data[col].isnull().sum()),
                    }
                )
            except (TypeError, ValueError) as e:
                print(f"Error occurred while updating metrics for column {col}: {e}")
                pass

            project_structure[col] = {
                "category": "context",
                "type": column_type,
                "metrics": metrics,
            }

        return project_structure

    # Project Samples
    def get_nb_samples(self) -> int:
        # This function returns the number of samples in the project
        return len(self.get_project_parquet())

    def get_samples_ids(self) -> list[str]:
        # This function returns the list of samples ids
        project_data = self.data
        return project_data["sample_id"].tolist()

    def get_data(self, samples_ids: list[str]) -> pd.DataFrame:
        # This function will be called when the user
        # wants to analyze data from your project

        # The function should return a pandas DataFrame
        # containing the data corresponding to the samples_ids
        print("ID:", len(samples_ids))
        project_data = self.data.set_index("sample_id")
        data = project_data.loc[samples_ids]
        print("Data:", data.shape)

        return data


provider = DataProvider()
provider.add_project(WeldingQualityMetadata())

# Finally, start the server
provider.start_server()
