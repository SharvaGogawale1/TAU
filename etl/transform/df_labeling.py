import pandas as pd
def labeling(_df: pd.DataFrame, _column_name_to_append: str, _values: list) -> pd.DataFrame:
    _df[_column_name_to_append]=_values
    return _df