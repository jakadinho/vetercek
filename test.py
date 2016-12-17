import numpy as np


my_list=np.arange(7, 38, 3)
my_list2=np.arange(38, 50, 1)
print np.concatenate((my_list, my_list2), axis=0)
