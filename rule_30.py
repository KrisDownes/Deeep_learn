import numpy as np 
import matplotlib.pyplot as plt

def initial_state(width):
    initial = np.zeros((1, width), dtype=int)
    if width % 2 == 0:
        initial = np.insert(initial, int(width / 2), values=0, axis=1)
        initial[0, int(width / 2)] = 1
        return initial
    else:
        initial[0, int(width / 2)] = 1
        return initial
def rule30(array):
    row1 = np.pad(array,[(0,0), (1,1)], mode='constant')
    next_row = array.copy()
    for x in range(1, array.shape[0]+1):
        for y in range(1, array.shape[1]+1):
            if row1[x-1][y-1] == 1 ^ (row1[x-1][y] == 1 or row1[x-1][y+1] == 1):
                next_row[x - 1, y - 1] = 1
            else:
                next_row[x - 1, y - 1] = 0
        return np.array(next_row)

def apply_rule(n):
    rv = initial_state(n)
    while rv[-1][0] == 0:
        rv = np.append(rv,rule30(rv[-1].reshape(1,-1)),axis=0)
        
    return rv
plt.figure(figsize=(10,6))
plt.imshow(apply_rule(1000), cmap='hot')
plt.show()
