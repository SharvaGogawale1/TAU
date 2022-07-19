import pandas as pd
from datetime import datetime

def features_extraction(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(columns="DoubleTime", inplace=True)
    df.drop(index=0, inplace=True)
    df["StringTime"] = [datetime.strptime(time[:time.find(".")], '%m/%d/%y  %H:%M:%S') for time in df["StringTime"]]
    df["StringTime"] = df.StringTime - df.StringTime.iloc[0] # setting base 0 for time comparission
    return df
