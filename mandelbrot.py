import math
import cmath
import numpy as np 
import matplotlib.pyplot as plt

def z(n,c):
    if n==0:
        return 0
    else:
        return z(n-1,c) **2 + c 

def complex_matrix(xmin,xmax,ymin,ymax,pixel_den):
    re = np.linspace(xmin,xmax,int((xmax-xmin)*pixel_den))
    im = np.linspace(ymin,ymax,int((ymax-ymin)* pixel_den))
    return re[np.newaxis,:] + im[:,np.newaxis] *1j
def is_stable(c,num_int):
    z=0
    for _ in range(num_int):
        z = z ** 2 + c 
    return abs(z) <=2
c = complex_matrix(-2,0.5,-1.5,1.5,pixel_den=512)
plt.imshow(is_stable(c,num_int=100),cmap="binary")
plt.gca().set_aspect("equal")
plt.axis("off")
plt.tight_layout()
plt.show()
