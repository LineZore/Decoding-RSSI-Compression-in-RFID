import numpy as np
import matplotlib.pyplot as plt
import math

#   Please modify these configurations to change the object of RSSI correction. 
#   For example, the following default configuration represents that the U8 tag 
#   corrected the RSSI at a distance of 2m with a reference distance of 4m.

#Select the tag, 0 for U8, 1 for R6P, and 2 for 9640
tind=0
#Reference distance for correcting RSSI, range 2-8m 
ref_dis=4
#Target distance, distance to correct RSSI, range 2-8m
target_dis=2
#Target tag, select one of the five tags of the same type, range 0-4
target_tag=0

file_path="./data/"
color_arr=['blue','green','red','purple','orange']
tag_name=['U8','R6P','9640']
distance=[2,3,4,5,6,7,8]
line_arr=['-','--','-.',':']
ref_dis_ind=distance.index(ref_dis)
target_dis_ind=distance.index(target_dis)
#The transmitting power of the reader
x_reader=[10.0+i*0.25 for i in range(91)]

tag_num=0
data=[]
file_name = f"{tag_name[tind]}.txt"
#Load data
with open(file_path+file_name, 'r') as file:
    tag_num_t=0
    for line in file:
        if line.strip() != '':
            # Remove the newline characters at the end of each line and separate them by spaces
            data.append( list(map(float,line.strip().split())))
            tag_num_t+=1
        else :
            tag_num=max(tag_num,tag_num_t)
            tag_num_t=0

tag_data=[[] for i in range(tag_num)]
k=[[] for i in range(tag_num)]      #Slope of linear fitting
b=[[] for i in range(tag_num)]      #Intercept of linear fitting

for i in range(len(data)):
    tag_data[i%tag_num].append(data[i])

for i in range(tag_num):
    x=np.array(x_reader)
    y=np.array(tag_data[i][ref_dis_ind])
    
    # Find the index that is not NaN
    mask = ~np.isnan(x) & ~np.isnan(y)

    x_clean = x[mask]
    y_clean = y[mask]

    coeffs = np.polyfit(x_clean, y_clean, 1)
    k[i],b[i]=coeffs

rssi_fix=[]
for i in range(len(tag_data[target_tag])):
    rssi=np.array(tag_data[target_tag][i])
    ptx=np.array(x_reader)
    # Find the index that is not NaN
    mask = ~np.isnan(ptx) & ~np.isnan(rssi)
    x_clean = ptx[mask]
    y_clean = rssi[mask]
    rssi_fix.append(y_clean+(1-k[target_tag])* x_clean-(1-k[target_tag])*x_clean[-1])   #rssi fix
    

rssi=np.array(tag_data[target_tag][target_dis_ind])
ptx=np.array(x_reader)
mask = ~np.isnan(ptx) & ~np.isnan(rssi)
x_clean = ptx[mask]
y_clean = rssi[mask]
y_ref=x_clean-x_clean[-1]+y_clean[-1]

#plot
plt.plot(x_clean, y_clean, label="Raw RSSI", linewidth=2)
plt.plot(x_clean, rssi_fix[target_dis_ind], label="Corrected RSSI", linewidth=2)
plt.plot(x_clean, y_ref, label="Ideal RSSI", linewidth=2)

plt.title(f"{tag_name[tind]},{target_dis}m",fontsize=18)
plt.xlabel("Ptx (dBm)",fontsize=18)
plt.ylabel("RSSI (dBm)",fontsize=18)
plt.tick_params(axis='both', labelsize=18)

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show() 

