import json
import numpy as np
import pandas as pd
import os


def extract_features(data: pd.DataFrame, phase: int):
    current_ang = data[f"I{phase} Ang"]
    voltage_ang = data[f"V{phase} Ang"]
    voltage = data[f"V{phase}"]
    current = data[f"I{phase}"]
    real_power = data[f"kW L{phase}"]
    thd = data[f"I{phase} THD"]

    impedance_ang = (voltage_ang - current_ang) * np.pi/180
    reactive_power = voltage * current * np.sin(impedance_ang)
    apparent_power = np.sqrt(reactive_power**2 + real_power**2)
    resistance = real_power / current**2
    reactance = reactive_power / current**2
    impedance = voltage / current
    distortion_factor = 1 / np.sqrt(1 + thd**2)

    features = {
        "reactive_power": reactive_power.tolist(),
        "apparent_power": apparent_power.tolist(),
        "resistance": resistance.tolist(),
        "reactance": reactance.tolist(),
        "impedance": impedance.tolist(),
        "distortion_factor": distortion_factor.tolist(),
        }

    with open(
        os.path.join(
            os.getcwd(),'etl','transform','extraction.json'),'w') as json_file:
        json.dump(features, json_file)