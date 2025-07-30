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

#Linear fitting
coeffs = np.polyfit(x_clean, y_clean, 1)
k,b=coeffs

#Fix RSSI
rssi_fix=(y_clean+(1-k)* x_clean-(1-k)*x_clean[-1])   

y_ref=x_clean-x_clean[-1]+y_clean[-1]

#plot
plt.plot(x_clean, y_clean, label="Raw RSSI", linewidth=2)
plt.plot(x_clean, rssi_fix, label="Corrected RSSI", linewidth=2)
plt.plot(x_clean, y_ref, label="Ideal RSSI", linewidth=2)

plt.xlabel("Ptx (dBm)",fontsize=18)
plt.ylabel("RSSI (dBm)",fontsize=18)
plt.tick_params(axis='both', labelsize=18)

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show() 


