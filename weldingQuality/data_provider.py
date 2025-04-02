import pandas as pd
import numpy as np
from debiai_data_provider import DebiAIProject, DataProvider


METADATA_PARQUET_FILE_PATH = "metadata/ds_meta.parquet"


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

        parquet_df = pd.read_parquet(METADATA_PARQUET_FILE_PATH)

        # Convert np.int64 to native Python int
        data = parquet_df.map(
            lambda x: int(x) if isinstance(x, (np.integer)) else str(x)
        )

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

        self.data = data

    # Project Info
    def get_structure(self) -> dict:
        # Load the data from the parquet file
        UNWANTED_COLUMNS = ["sample_id"]

        # Create the structure
        project_structure = {}

        for col in self.data.columns:
            if col in UNWANTED_COLUMNS:
                continue

            project_structure[col] = {
                "category": "context",
                "type": "auto",
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
        print(project_data)
        data = project_data.loc[samples_ids]
        print(data)
        print(len(data))

        return data


provider = DataProvider()
provider.add_project(WeldingQualityMetadata())

# Finally, start the server
provider.start_server()
