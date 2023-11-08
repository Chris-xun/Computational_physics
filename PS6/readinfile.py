import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# use pandas
df = pd.read_csv('events.csv')
df_2to3 = df[(df['q2'] > 2) & (df['q2'] < 3)]
print(df_2to3)

# or, if you prefer numpy
mydata = np.genfromtxt('C:/Users\yx200\Desktop\imperial\yr3\computational_physics\PS6\events.csv', delimiter=',', skip_header=1)
# column 0 : q2, column 1 : ctk
q2column=0
mydata_2to3 = mydata[(mydata[:, q2column] > 2) & (mydata[:, q2column] < 3)]
print(mydata_2to3)
print(mydata_2to3.shape)
