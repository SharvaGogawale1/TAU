import json
from scipy.signal import find_peaks

T_ABS= 0.15
MINIMAL_DISTANCE_BETWEEN_PLOTS=30

def state_detection(array_to_analyze: list,path_to_save : str) -> None:
    separated_events = {}
    state_index_numpy_array, _ = find_peaks(
        abs(array_to_analyze),
        height=T_ABS,
        distance=MINIMAL_DISTANCE_BETWEEN_PLOTS
        )
    state_index_list = state_index_numpy_array.tolist()
    for index in range(len(state_index_list)):
        try:
            separated_events["state_" + str(index)] = {
                "start_time": state_index_list[index],
                "end_time": state_index_list[index + 1],
            }
        except:
            pass
    with open(path_to_save, 'w') as json_file:
        json.dump(separated_events, json_file)
