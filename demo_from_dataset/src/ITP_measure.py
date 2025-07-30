import numpy as np
import matplotlib.pyplot as plt

#   Please modify these configurations to measure the interrogation threshold power(ITP) 
#   for different readers and tags.For example, the following default configuration states 
#   that the U8 tag establishes a lookup table with 2m as a reference and outputs the  
#   result of ITP measurement at other distances.

#Select the tag, 0 for U8, 1 for R6P, and 2 for 9640
tind=0
#Reference distance for constructing the lookup table, range 2-8m
ref_dis=2
#Target tag, select one of the five tags of the same type, range 0-4
target_tag=0

#File path
file_path="./data/"
color_arr=['red','yellow','orange','green','blue']
tag_name=['U8','R6P','9640']
distance=[2,3,4,5,6,7,8]
#The transmitting power of the reader
x_reader=[10.0+i*0.25 for i in range(91)]

ref_dis_ind=distance.index(ref_dis)
pj_measure=[[] for i in range(len(tag_name))]

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
pj=[[] for i in range(tag_num)]

for i in range(len(data)):
    tag_data[i%tag_num].append(data[i])

for i in range(tag_num):
    x=np.array(x_reader)
    y=np.array(tag_data[i][ref_dis_ind])
    # Find the index that is not NaN
    mask = ~np.isnan(x) & ~np.isnan(y)
    x_clean = x[mask]
    y_clean = y[mask]

    #The ITP is the first non-zero transmission power
    pj[i]=x_clean[0]
    
pj_mean=[[] for i in range(len(distance))]

#Construct a lookup table based on the data obtained at the given reference distance
ref_y=[-a1-b1 for a1,b1 in zip(x_reader,tag_data[target_tag][ref_dis_ind])]
pj_real=[0 for i in range(len(distance))]

for j in range(len(tag_data[target_tag])):
    
    # if j!=ref_dis_ind :
    x=np.array(x_reader)
    y=np.array(tag_data[target_tag][j])
    
    # Find the index that is not NaN
    mask = ~np.isnan(x) & ~np.isnan(y)
    x_clean = x[mask]
    y_clean = y[mask]
    pj_real[j]=x_clean[0]

    # Perform ITP measurement for each RSSI
    for ii in range(len(x_clean)):
        rssi_pj=-y_clean[ii]-x_clean[ii]
        # Look up in the lookup table
        for idx, val in enumerate(ref_y):
            if not np.isnan(val) and val <= rssi_pj:
                pj_fix=x_clean[ii]-(x_reader[idx]-pj[target_tag])        # One-shot ITP Measurement
                
                pj_mean[j].append(pj_fix)
                break

pj_measure[tind]=[sum(lst) / len(lst) if len(lst) > 0 else 0 for lst in pj_mean]

#plot
width = 0.35   
x = np.arange(len(distance))  

plt.bar(x - width/2, pj_real, width, label='Ground Truth')
plt.bar(x + width/2, pj_measure[tind], width, label='In-situ Measurement')

plt.xlabel('Distance (m)')
plt.ylabel('ITP (dBm)')
plt.title('In-situ Measurement and Ground Truth')
plt.xticks(x, distance)
plt.legend()

plt.show()