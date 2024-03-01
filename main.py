import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

vbias = 29.5
muons_per_min = 25 * 5 #Intensity of muons is 1 per cm^2 per minute, area is 25cm x 5cm
thres_volt = 650

#Set current directory
current_directory = os.getcwd()

#Get a list of all the items inside of the directory
entries = os.listdir(current_directory)

#Add entries to a list of files if the entry is a file!
files = [f for f in entries if os.path.isfile(os.path.join(current_directory,f))]

files_sanitised = [] #Contains only the voltages numbers on the file
files_csv = []

#Find all .csv files and append to list. Also strip the A.csv from each.
for file in files:
    if '.csv' in file:
        df = pd.read_csv(file)
        count = df[' count0 ']
        #Make sure that there is more than one time entry!
        if len(count) > 1:
            file_stripped = ''.join(letter for letter in file if letter.isdigit())
            files_csv.append(file)
            files_sanitised.append(file_stripped)

minutes = [] #Stores time values in minutes

#Count values for each of the coincidences
counts_0 = []
counts_1 = []
counts_2 = []
counts_3 = []
counts_4 = []
counts_5 = []



#Add the numerical value from the sanitised list to the voltages array
for i in files_sanitised:
    minutes.append(int(i)) #Minutes passed as integer values


#Extracting data from each of the files. See photo for coincidence setup

for file in files_csv:
    df = pd.read_csv(file)
    time = df[' time ']

    #Different coincidence count rates
    count0 = df[' count0 ']
    count1 = df[' count1 ']
    count2 = df[' count2 ']
    count3 = df[' count3 ']
    count4 = df[' count4 ']
    count5 = df[' count5 ']

    counts_0.append((count0[len(count0)-1]-count0[0]))
    counts_1.append((count1[len(count1)-1]-count1[0]))
    counts_2.append((count2[len(count2)-1]-count2[0]))
    counts_3.append((count3[len(count3)-1]-count3[0]))
    counts_4.append((count4[len(count4)-1]-count4[0]))
    counts_5.append((count5[len(count5)-1]-count5[0]))

expected = []

for min in minutes:
    expected.append(min*muons_per_min)

fig, ax = plt.subplots()

#Store in dictionary!
count_list = {
    'A&&B&&C&&D': counts_0, 
    '(A||B)&&(C||D)': counts_1, 
    '(A&&B)||(C&&D)': counts_2, 
    'Any single SiPM': counts_3, 
    'Any two SiPMs': counts_4, 
    'Any Three SiPMS': counts_5
    }

colors = ['r','b','g','k','m','c']

for i, (key, values) in enumerate(count_list.items()):
    ax.plot(minutes, values, label=key, color=colors[i])

#Expected muon line
ax.scatter(minutes, expected, label='Expected count')

ax.set_yscale('log')
ax.set_xlabel('Time / Minutes')
ax.set_ylabel('Counts')
ax.set_title(f'Coincidence Counts vs Time, Vbias = {vbias}V, Thresh Vol={thres_volt}mV')
ax.legend()
plt.savefig('coincidence_test_function_of_time')
plt.show()

###############################
#      EFFICIENCY GRAPH       #
# Uses data from 8 Min capure #
###############################

mins = 8
fig1, ax1 = plt.subplots()

coincidences = []
efficiencies = []

for i, (key, values) in enumerate(count_list.items()):
    final_index = len(values) - 1
    counts_8_mins = values[final_index]
    expected_8_mins = expected[final_index]
    fraction = counts_8_mins / expected_8_mins
    efficiency = np.round(fraction * 100, 4)

    coincidences.append(key)
    efficiencies.append(efficiency)

efficiency_100 = np.full_like(efficiencies, 100, dtype=float)

ax1.plot(coincidences, efficiency_100, label = f'100% Efficiency', color = 'r', ls = '--')
ax1.bar(coincidences, efficiencies)
ax1.set_title(f'Efficiency Est., {mins} mins, VBias={vbias}V, Thresh Vol={thres_volt}mV')
ax1.set_xlabel('Coincidence Logic')
ax1.legend()
ax1.set_ylabel('Efficiency Est. % (Obs count / Exp count)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('efficiency_bars')
plt.show()


    