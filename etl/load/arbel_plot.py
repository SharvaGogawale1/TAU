import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime
from scipy.signal import savgol_filter
from matplotlib_inline.backend_inline import set_matplotlib_formats
set_matplotlib_formats('svg')


COLORS_LIST = ["blue","red", "green"]


def plot_param(params: list,phase: int,data: pd.DataFrame, _window_length: int, _polyorder: int) -> None:
    plt.figure()
    for index, param in enumerate(params, start=0):
        if(param == "I"):
            columns_list = ["StringTime", "I1", "I2", "I3"]#["StringTime","I2 Mag"]#["StringTime", "I1", "I2", "I3"]
            df = pd.DataFrame(data, columns=columns_list)
            if phase==1:
                dfs = [df.I1]
            elif phase==2:
                dfs = [df.I2]
            elif phase==3:
                dfs = [df.I3]
            else:
                dfs =[df.I1, df.I2, df.I3]# [df.values[:,1]]#[df.I1, df.I2, df.I3]
            suptitle=("Current(t)")
            title= 'I'
            units= 'A'
        elif(param == "P"):
            columns_list = ["StringTime", "kW L1", "kW L2", "kW L3"]# ["StringTime", "kW"] #["StringTime", "kW L1", "kW L2", "kW L3"]
            df = pd.DataFrame(data, columns=columns_list)
            if phase==1:
                dfs = [df.values[:, 1]]
            elif phase==2:
                dfs = [df.values[:, 2]]
            elif phase==3:
                dfs = [df.values[:, 3]]
            else:
                dfs = [df.values[:,1], df.values[:,2], df.values[:,3]]
            suptitle=("P(t)")
            title= 'P'
            units = 'kW'
        elif (param == "THD"):
            columns_list = ["StringTime", "I1 THD", "I2 THD", "I3 THD"]#["StringTime", "I2 THD"]#["StringTime", "I1 THD", "I2 THD", "I3 THD"]
            df = pd.DataFrame(data, columns=columns_list)
            dfs = [df.values[:,1], df.values[:,2], df.values[:,3]]#[df.values[:,1]]#[df.values[:,1], df.values[:,2], df.values[:,3]]
            suptitle=("THD(t)")
            title = 'THD'
            units = '%'
        #-------#
        time =[datetime.min+time for time in df.StringTime]
        plt.subplot(len(params), 1, index+1)
        data_vector = savgol_filter(dfs[0], window_length=_window_length, polyorder=_polyorder)
        plt.step(time, data_vector, color=COLORS_LIST[index])
        plt.xlabel("[H:MM]")
        plt.ylabel(f"[{units}]")
        plt.title(title)
        plt.gcf()#.autofmt_xdate()
        plt.xticks(time[0:len(time):max(int(len(time)/8),1)])  # how many x values to display
        myFmt = mdates.DateFormatter('%H:%M')
        plt.gca().xaxis.set_major_formatter(myFmt)
    plt.suptitle('Current, Power & THD')
    plt.tight_layout()
    plt.show()
