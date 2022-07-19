import pandas as pd

def date_parse_to_string_format(raw_list: pd.core.frame.DataFrame) -> list:
    return [date_sample[date_sample.rfind(" ")+len(" "):] for date_sample in raw_list.apply(str)]