import pandas as pd
import os

def extract_df_from_file(filename: str, sep_attempt: str) -> pd.DataFrame:
    try:
        return pd.read_csv(filename, sep=sep_attempt)
    except:
        raise Exception("File read failed")

def extract_df_from_file_correcting_path(initial_path: str,filename: str, sep_attempt: str) -> pd.DataFrame:
    try:
        return pd.read_csv(os.path.join(initial_path, 'data', filename), sep=sep_attempt)
    except:
        raise Exception("File read failed")
