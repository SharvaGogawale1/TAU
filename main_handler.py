#--------MAIN----------#
# project imports
from etl.extract.extract import extract_df_from_file_correcting_path
from etl.extract.extract import extract_df_from_file
from etl.extract.extract_filename_full_path import get_db, get_tables, get_file
from etl.extract.get_state import get_state
from etl.transform.features import features_extraction
from etl.transform.date_parse_to_string import date_parse_to_string_format
from etl.transform.filter_noise import filter_noise
from etl.transform.generate_plotly_graph import generate_plotly_figure
from etl.load.state_detection.state_detection import state_detection

# Local python imports
import os

# 3rd party imports
import pandas as pd
import numpy as np

#Global Variables
LABELING_FILENAME="train_op_labeling.json"
LABELING_PATH="data"

class extract:
    FILENAME_TO_EXTRACT = "data2.csv"
    @staticmethod
    def extract_pandas(_filename: str,sep_attempt: str = ";") -> pd.DataFrame:
        return extract_df_from_file(filename=_filename,sep_attempt=sep_attempt)

    @staticmethod
    def get_database() -> list:
        return get_db()

    @staticmethod
    def get_table(db: str) -> list:
        return get_tables(db).split(", ")

    @staticmethod
    def get_filename(db: str, table: str) -> str:
        return get_file(db, table)

    @staticmethod
    def get_state(path: str) -> dict:
        return get_state(file_path=path)

class transform:
    @staticmethod
    def clean_df(df: pd.DataFrame) -> pd.DataFrame:
        return features_extraction(df)

    @staticmethod
    def clean_noise(raw_list: list, _window: int = None, _poly: int = None) -> list:
        if _window:
            if _poly:
                return filter_noise(_raw_data_list=raw_list, _window=_window, _polyorder=_poly)
            return filter_noise(_raw_data_list=raw_list, _window=_window)
        return filter_noise(_raw_data_list=raw_list)

    @staticmethod
    def convert_date_samples(date_samples_to_filter) -> list:
        return date_parse_to_string_format(raw_list=date_samples_to_filter)

    @staticmethod
    def generate_figure(time_sample: list, dict_values: dict, state_value: dict = {}):
        return generate_plotly_figure(
            time_samples=time_sample,
            dict_values=dict_values,
            state_dict=state_value
        )

class load:
    STATE_FILE_PATH = os.path.join(os.getcwd(),'data','state_detection.json')
    @staticmethod
    def generate_state(_array: np.ndarray, _path_to_save: str = STATE_FILE_PATH) -> None:
        state_detection(array_to_analyze=_array, path_to_save=_path_to_save)
