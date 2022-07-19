from etl.extract.extract_filename_full_path import extract_data
from etl.extract.extract import extract_df_from_file
#from etl.transform.features import features_extraction
from etl.load.arbel_plot import plot_param
# from etl.transform.stage_detection.stage_detection import event_detection
from etl.transform.extract_features import extract_features

import pandas as pd

class extract:
    @staticmethod
    def get_filename() -> str:
        return extract_data()

    @staticmethod
    def extract_pandas(filename: str, sep_attempt: str = ";") -> pd.DataFrame:
        return extract_df_from_file(filename=filename,sep_attempt=sep_attempt)

class transform:
    @staticmethod
    def clean_df(df: pd.DataFrame) -> pd.DataFrame:
        return features_extraction(df)
    
    @staticmethod
    def write_output_json_extract_features(df: pd.DataFrame, phase: int) -> None:
        extract_features(df, phase)
        
    @staticmethod
    # def write_output_json_event_detection(df: pd.DataFrame, phase: int) -> None:
    #     event_detection(df, phase)

    @staticmethod
    def filter_savigol(df: pd.DataFrame) -> pd.DataFrame:
        pass


class load:
    @staticmethod
    def generate_matplotlib(df: pd.DataFrame = None) -> None:
        file_name='washin' #microwave
        if file_name=='microw' or file_name=='toaste' or file_name=='dryer':
            phase=1
        elif file_name=='tami4' or file_name=='dishwa' or file_name=='boiler':
            phase=2
        elif file_name=='washin':
            phase=3

        params = ['I','P','THD']#['P','E']
        plot_param(params,phase,df, _window_length=11, _polyorder=3)


def main() -> None:
    FILENAME = extract.get_filename()
    try:
        transform.write_output_json_event_detection(
                transform.clean_df(extract.extract_pandas(filename=FILENAME)), 3
            )
    except KeyError:
        transform.write_output_json_event_detection(
                transform.clean_df(extract.extract_pandas(filename=FILENAME, sep_attempt=",")), 3
            )

if __name__ == "__main__":
    main()

