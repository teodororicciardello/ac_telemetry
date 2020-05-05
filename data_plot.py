#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import argparse
from datetime import date


labels=['position', 'speed', 'time', 'gas', 'brake', 'gear', 'lap']
metric_params={
    'speed': {'offset': -100 ,'scale': 0, 'limit': 250, 'spacing': 25},
    'gas': {'offset': -2.5, 'scale': 1.2, 'limit': 5, 'spacing': 0.2},
    'brake': {'offset': -2.5, 'scale': 1.2, 'limit': 5, 'spacing': 0.2},
    'gear': {'offset': 0, 'scale': 7, 'limit': 20, 'spacing': 1}
}
lap_sel_1=-1
lap_sel_2=-1
data=[]
#metrics={}
#metrics['speed']=[]## list of numbers from file

### Select laps
def select_laps(first, second):
    print('Lap times:')
    if len(data) > 0:
        for i in range(0, len(data)):
            time=data[i]['time'][len(data[i]['time'])-1]
            l = data[i]['lap'][len(data[i]['lap'])-1]+1
            print('(%d) lap %d: ' % ((i+1), l), str(int(int(time/1000)/60))+':'+str(int(time/1000) % 60).zfill(2)+':'+str(time % 1000).zfill(3))
    else: print('Error - Data not loaded!')
    first=int(input('Select first lap (default: %d): ' % first) or first) ### TODO implement error handling
    second=int(input('Select second lap (default: %d): ' % second) or second)
    return(first, second)

### Select metrics
def select_metrics(first, second):
    metrics=['speed', 'gas', 'brake', 'gear']
    print('Metrics available:')
    for i in range(0,len(metrics)):
        print('%d: %s' % (i, metrics[i]))
    first=int(input('Select metric id (default: %s): ' % first) or first) ### 20200505_lap11.csv
    second=int(input('Select metric id (default: %s): ' % second) or second)
    return(metrics[first], metrics[second])

### present plot
def plot_laps(label_1, label_2, ref1, lap1_metric1, lap1_metric2, 
                ref2, lap2_metric1, lap2_metric2,):
    
    ### TODO add labels for the laps presented (time), improve presentation
    
    fig, ax1 = plt.subplots()
    
    ### set x axis
    ax1.set_xlabel('position (track %)')  ## convert to 100%
    ax1.set_xlim(0.0, 1.0) ## convert to 100%
    major_ticks = np.arange(0, 1.0, 0.1)
    ax1.set_xticks(major_ticks)
    ax1.grid(axis='both')

    ### set first metric (y axis)
    color = 'r-'
    ax1.set_ylabel(label_1, color='tab:red')
    ax1.set_ylim(metric_params[label_1]['offset'], metric_params[label_1]['limit'])##TODO
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_yticks(np.arange(0, metric_params[label_1]['limit'], metric_params[label_1]['spacing']))## TODO
    ax1.set_yticks(np.arange(0, metric_params[label_1]['limit'], 5), minor=True)##TODO

    ax1.plot(ref1, lap1_metric1, color, ref2, lap2_metric1, 'r--')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'b-'
    ax2.set_ylabel(label_2, color='tab:blue')  # we already handled the x-label with ax1
    ax2.set_ylim(0, metric_params[label_2]['limit'])
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.set_yticks(np.arange(0, metric_params[label_2]['scale'], metric_params[label_2]['spacing']))

    ax2.plot(ref1, lap1_metric2, color, ref2, lap2_metric2, 'b--')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.grid(axis='y')
    plt.show()

def save_lap(default):
    print('Select lap to save:')
    if len(data) > 0:
        for i in range(0, len(data)):
            time=data[i]['time'][len(data[i]['time'])-1]
            l = data[i]['lap'][len(data[i]['lap'])-1]+1
            print('(%d) lap %d: ' % ((i+1), l), str(int(int(time/1000)/60))+':'+str(int(time/1000) % 60).zfill(2)+':'+str(time % 1000).zfill(3))
    else: 
        print('Error - Data not loaded!')
        exit() ### TODO 
    lap=int(input('Select the lap to save (default: %d): ' % default) or default)
    default_file = date.today().strftime("%Y%m%d")+'_lap'+str(data[lap-1]['lap'][len(data[lap-1]['lap'])-1]+1)+'.csv'
    filename=input('insert name of the file (default: %s): ' % default_file) or default_file
    with open(filename, 'w') as writer: ### TODO move loop into a separate function
        for i in range(0,len(data[lap-1]['position'])):
            line=''
            line += str(data[lap-1]['position'][i])+';'
            line += str(data[lap-1]['speed'][i])+';'
            line += str(data[lap-1]['time'][i])+';'
            line += str(data[lap-1]['gas'][i])+';'
            line += str(data[lap-1]['brake'][i])+';'
            line += str(data[lap-1]['gear'][i]+1)+';'## to match the right gear
            line += str(data[lap-1]['lap'][i])+'\n'
            writer.write(line)
        ### add the end of lap line (prevent error in reading the file standalone)
        writer.write('0.00000;0.0;0;0.0;0.0;0;0\n')


####### Main program  ##########

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot data for AC laps")
    parser.add_argument("-d", "--data", help="file with lap data")
    args=parser.parse_args()
    data_file=args.data

    ## initialise variables
    count=0
    last_position=2.0
    last_lap =-1
    best_lap =-1
    best_time=90000000
    ## read data
    with open(data_file, 'r') as reader: ### TODO move loop into a separate function
        for line in reader:
            current_lap=int(line.split(';')[6])
            current_position=float(line.split(';')[0])
            ##if current_lap != last_lap: ## just changed lap
            if (current_position < last_position and last_position > 0.99) : ## just changed lap or it's first lap
                count+=1
                if last_lap != -1:  ## not execute on first lap loaded
                    data.append(metrics)
                    if best_time > metrics['time'][len(metrics['time'])-1]: ## set best_time
                        best_time= metrics['time'][len(metrics['time'])-1]
                        best_lap=count-1
                metrics=dict(zip(labels, [[],[],[],[],[],[],[]]))
            ## TODO optimise read from file
            metrics['position'].append(float(line.split(';')[0]))
            metrics['speed'].append(float(line.split(';')[1]))
            metrics['time'].append(int(line.split(';')[2]))
            metrics['gas'].append(float(line.split(';')[3]))
            metrics['brake'].append(float(line.split(';')[4]))
            metrics['gear'].append(int(line.split(';')[5])-1)## to match the right gear
            metrics['lap'].append(current_lap)
            last_lap=current_lap
            last_position=current_position

    laps_count=count-1 ## last lap in file do not count
    best_time_s= str(int(int(best_time/1000)/60))+':'+str(int(best_time/1000) % 60)+':'+str(best_time % 1000)

    laps_prompt='''Laps loaded: %d
    Best lap time (%d): %s
    '''
    print(laps_prompt % (laps_count, best_lap, best_time_s))

    ##' Defaults for shell prompt'
    lap_sel_1=best_lap
    lap_sel_2=laps_count
    metric_1='speed'
    metric_2='gear'

    selection_prompt=''' Select one of the following options:
    (P) Plot laps (%d vs %d)
    (L) Select laps to compare
    (M) Select metric(s) to present (current: %s & %s)
    (S) Save a lap on file
    (L) Load a lap from file (added at the end)
    (Q) Quit Application
    '''

    while 1:
        print(selection_prompt % (lap_sel_1, lap_sel_2, metric_1, metric_2))
        inp = input('? ')
        if inp in ('P', 'p'):### TODO optimize selection (switch?)
            plot_laps(metric_1, metric_2, 
                data[lap_sel_1-1]['position'], data[lap_sel_1-1][metric_1], data[lap_sel_1-1][metric_2],
                data[lap_sel_2-1]['position'], data[lap_sel_2-1][metric_1], data[lap_sel_2-1][metric_2])
        if inp in ('L','l'):
            lap_sel_1, lap_sel_2 = select_laps(lap_sel_1, lap_sel_2)
        if inp in ('M','m'):
            metric_1, metric_2 = select_metrics(metric_1, metric_2)
        if inp in ('S', 's'):
            save_lap(lap_sel_1)
        if inp in ('L', 'l'): ## TODO
            print('WIP - Function not implemented yet')
        if inp in ('Q', 'q'):
            exit()
        if inp not in ('P','Q', 'S', 'L','M'):
            print('Selection not valid')
