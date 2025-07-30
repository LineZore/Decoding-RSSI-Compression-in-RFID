import numpy as np
import matplotlib.pyplot as plt

#File path
file_path="./data/"
#The transmitting power of the reader
x_reader=[10.0+i*0.25 for i in range(91)]

ref_data=[]
ver_data=[]

#Load data
with open(file_path+'ref.txt', 'r') as file:
    first_line = file.readline().strip()
    ref_data=( list(map(float,first_line.strip().split())))

with open(file_path+'ver.txt', 'r') as file:
    first_line = file.readline().strip()
    ver_data=( list(map(float,first_line.strip().split())))

# Find the index that is not NaN
x=np.array(x_reader)
y=np.array(ref_data)
mask = ~np.isnan(x) & ~np.isnan(y)
x_clean = x[mask]
y_clean = y[mask]

#The ITP is the first non-zero transmission power
pj=x_clean[0]

#Construct a lookup table based on the data obtained at the given reference distance
ref_y=[-a1-b1 for a1,b1 in zip(x_reader,ref_data)]

pj_mean=[]

x=np.array(x_reader)
y=np.array(ver_data)

# Find the index that is not NaN
mask = ~np.isnan(x) & ~np.isnan(y)
x_clean = x[mask]
y_clean = y[mask]

pj_real=x_clean[0]
# Look up in the lookup table
for i in range(len(x_clean)):
    rssi_pj=-y_clean[i]-x_clean[i]
    for idx, val in enumerate(ref_y):
        if not np.isnan(val) and val <= rssi_pj:
            pj_fix=x_clean[i]-(x_reader[idx]-pj)        # One-shot ITP Measurement
            pj_mean.append(pj_fix)
            break

#Calculate the average result
pj_measure=sum(pj_mean) / len(pj_mean) 

print('Using ref.txt as a reference, perform in-situ measurement on each RSSI in ver.txt, and the final average results are as follows:')
print('Ground Truth:',pj_real,'dB')
print('Average ITP:',pj_measure,'dB')

#plot
# width = 0.35   
# x = np.arange(len(pj_mean))  
# pj_plot_real=[pj_real for i in range(len(pj_mean))]

# plt.bar(x - width/2, pj_plot_real, width, label='Ground Truth')
# plt.bar(x + width/2, pj_mean, width, label='In-situ Measurement')

# plt.xlabel('Distance (m)')
# plt.ylabel('ITP (dBm)')
# plt.title('In-situ Measurement and Ground True')
# # plt.xticks(x, distance)
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
# plt.tight_layout()
# plt.show()