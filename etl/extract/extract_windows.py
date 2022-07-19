import pandas as pd
import os

def get_dataframe_from_csv(csv_filename: str) -> pd.DataFrame:
    return pd.read_csv(
        os.path.join(
            os.getcwd(),
            'data',
            csv_filename)
    )