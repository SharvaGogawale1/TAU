import csv, pyodbc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import dateutil
from scipy import ndimage
import os
def gen_CSV(MDB):
    os.getcwd()
    # connect to db
    # con = pyodbc.connect(
    #     r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+MDB+';')
    # cur = con.cursor()
    # colDesc = list(cur.columns())
    # table_names=[]
    # for b in colDesc:
    #     if (b[2] not in table_names):
    #         table_names.append(b[2])
    # c=[e for e in table_names if e[0:3]=='RT ']
    # # c= table_names[-1]
    # # c = table_names[3:]
    # rows = []
    # for i,c in enumerate([e for e in table_names if e[0:3]=='RT ']):
    #     SQL = 'SELECT * FROM [{}]'.format(c)
    #     cur.execute(SQL)
    #     if i==0: rows.append([x[3] for x in colDesc if x[2] == c])   #headers
    #     for row in cur.fetchall():
    #         if row[0]!=0.0:
    #             rows.append(row)
    #     del rows[1]                                         #remove first row


    # with open('data.csv', 'w', newline='') as fou:
    #     csv_writer = csv.writer(fou)  # default field-delimiter is ","
    #     csv_writer.writerows(rows)
    # cur.close()
    # con.close()

def calc_phase_energy(phase):
    phase= phase-1      #match an index
    col_list_power =["kW L1", "kW L2", "kW L3"]# ["kW L2"]#["kW L1", "kW L2", "kW L3"]
    df = pd.read_csv("data.csv", usecols=col_list_power)
    E= []
    sum = 0
    for x in range(df.shape[0]):
        sum = sum + df[col_list_power[phase]][x]
        E.append(sum)
    return(E)

def calc_energy():
    E= []
    for i in range(1,4):
        E.append(calc_phase_energy(i))
    return(np.array(E))


def get_data(path,file_name):       #also adds the Energy colums.
    gen_CSV(r'{}\{}.mdb'.format(path,file_name))
    with open('data.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    data = np.array(data)
    #add the energy columns
    #E=np.transpose(calc_energy())
    #E_titels= np.array(['E1','E2','E3'])
    #E_tot= np.vstack( (E_titels , E ))
    #data= np.hstack((data,E_tot))
    return(data)

def dilute_sampales(data,new_gap):
    Ts_orig= 1           # the original gap between samples [sec]
    k= int(new_gap/Ts_orig)
    n= int((len(data)-1)/k)
    new_data = [data[k*i] for i in range(1,n+1)]
    new_data.insert(0,data[0])
    return(new_data)
    elif(param == "P"):
        columns = ["StringTime", "kW L1", "kW L2", "kW L3"]# ["StringTime", "kW"] #["StringTime", "kW L1", "kW L2", "kW L3"]
        df = pd.read_csv("data.csv", usecols=columns)
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
        columns = ["StringTime", "I1 THD", "I2 THD", "I3 THD"]#["StringTime", "I2 THD"]#["StringTime", "I1 THD", "I2 THD", "I3 THD"]
        df = pd.read_csv("data.csv", usecols=columns)
        dfs = [df.values[:,1], df.values[:,2], df.values[:,3]]#[df.values[:,1]]#[df.values[:,1], df.values[:,2], df.values[:,3]]
        suptitle=("THD(t)")
        title = 'THD'
        units = '%'
    # elif (param == "E"):
    #     columns = ["StringTime", "E1", "E2", "E3"]
    #     df = pd.read_csv("data.csv", usecols=columns)
    #     dfs = [df.values[:, 1], df.values[:, 2], df.values[:, 3]]
    #     suptitle=("E(t)")
    #     title = 'E'
    #     units = 'Kwh'
    # elif (param == "dE"):
    #     columns = ["StringTime", "dE1", "dE2", "dE3"]
    #     df = pd.read_csv("data.csv", usecols=columns)
    #     dfs = [df.values[:, 1], df.values[:, 2], df.values[:, 3]]
    #     suptitle= ("dE(t))")
    #     title = 'dE'
    #     units = 'Kwh'
    #-------#
    if (Ts>=30):
        if(Ts %60 ==0):
            s_Ts= '{}[min]'.format(int(Ts/60))
        else:
            s_Ts = '{}[min]'.format(Ts / 60)
    else:
        s_Ts = '{}[sec]'.format(int(Ts))
    plt.suptitle('{}, Ts= {}'.format(suptitle, s_Ts))
    colors= ["blue","red", "green"]
    time= df.StringTime
    time = [time[i][10:18] for i in range(len(time))]   # keep the '%H:%M:%S' only.
    time = [dateutil.parser.parse(s) for s in time]
    if phase==1 or phase==2 or phase==3:
        num_of_phases=1
    for i in range(num_of_phases):
        plt.subplot(num_of_phases, 1, i+1)
        plt.step(time, dfs[i], color=colors[i])         # 'step' is the zero order interpolation plot function.
        plt.xlabel("t [h:m]")
        plt.ylabel("[{}]".format(units))
        plt.title("{}{}".format(title,i + 1))
        plt.xticks(time[0:len(time):max(int(len(time)/8),1)])  # how many x values to display
        plt.gcf()
        myFmt = mdates.DateFormatter('%H:%M')
        plt.gca().xaxis.set_major_formatter(myFmt)
    plt.tight_layout()

def gen_plots(params,phase, data, Ts=1):
    update_data(data, Ts)
    for x in params:
        plt.figure()
        plot_param(x,phase, Ts)


def calc_energy_diffs(data):
    E= data[1:, [-3,-2,-1]]
    E = E.astype(float)
    E = np.transpose(E)
    deltas= np.diff(E)
    E[:,1:E.shape[1]] =deltas
    E[:, 0] = 0
    return(E)

def update_data(data,Ts):   #adds the Energy diff between the sampels & dilutes the sampales
    if(Ts !=1):
        data=dilute_sampales(data, Ts)
    data = np.array(data)
    # calc_energy_deltas
    dE = np.transpose(calc_energy_diffs(data))
    dE_title = np.array(['dE1', 'dE2', 'dE3'])
    dE_tot = np.vstack((dE_title, dE))
    new_data = np.hstack((data, dE_tot))
    with open('data.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(new_data)

def dilute_sampales(data,new_gap):
    Ts_orig= 1           # the original gap between samples [sec]
    k= int(new_gap/Ts_orig)
    n= int((len(data)-1)/k)
    new_data = [data[k*i] for i in range(1,n+1)]
    new_data.insert(0,data[0])
    return(new_data)



#--------MAIN----------#

###-USER NEEDS TO CHANGE-###
path= os.getcwd()
###-select MDB file name-###
#file_name = '2bashsarsComputers\\low\\2'
# path='C:\\Users\\user\\Documents\\arbel\\event_detection\\'
file_name='washin' #microwave
if file_name=='microw' or file_name=='toaste' or file_name=='dryer':
    phase=1
elif file_name=='tami4' or file_name=='dishwa' or file_name=='boiler':
    phase=2
elif file_name=='washin':
    phase=3

#####
data= get_data(path ,file_name)
####-Original Data-######
params = ['I','P']#['P','E']
gen_plots(params,phase,data)
#####-Diluted Data-######
# d_params = ['P','dE']
# Ts= 0.5*60 #[sec]
# gen_plots(d_params,data,Ts)
#####
plt.show()


