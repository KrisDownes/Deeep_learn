#!/usr/bin/env python3

import time 
import numpy as np 

N = 1048

if __name__ == "__main__":
    A = np.random.randn(N,N).astype(np.float32)
    B = np.random.randn(N,N).astype(np.float32)

    flop = N*N*2*(N-1)
    

    start = time.monotonic()

    C = A @ B 

    end = time.monotonic()
    s = end - start
    print(f"{flop/s* 1e-9:.2f} GFLOPS")
    print(f"{flop/s * 1e-12:.2f} TFLOPS")
    

