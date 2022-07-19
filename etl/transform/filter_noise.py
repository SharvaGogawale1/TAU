from scipy.signal import savgol_filter

WINDOW_LENGTH = 19
POLY_ORDER = 3

def filter_noise(_raw_data_list: list, _window: int = WINDOW_LENGTH, _polyorder: int = POLY_ORDER) -> list:
    return savgol_filter(
        _raw_data_list,
        window_length=_window,
        polyorder=_polyorder
    )