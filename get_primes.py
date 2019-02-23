import numpy as np
import time

n = 6000000
start_time = time.time()
num = np.arange(3,n,2) #take out all the evens

for i in range(0,len(num)):
     prime_len = len(num)
     num = np.delete(num,np.where(num%num[i]==0)[0][1:])
     length_diff = prime_len - len(num)
     if length_diff == 0:
         break

print len(num),"time:",time.time()-start_time,"sec"
