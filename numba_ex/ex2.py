import time
import random
import numba
import numpy as np

@numba.njit
def single_threaded(arr):
    width, height = arr.shape
    out = np.zeros_like(arr)
    for i in range(height):
        for j in range(width):
            out[j,i] = random.random()

@numba.njit
def parallelized(arr):
    width, height = arr.shape
    out = np.zeros_like(arr)
    for i in range(height):
        for j in range(width):
            out[j,i] = random.random()

def main(N):
    cube = np.arange(N * N * N, dtype=float).reshape(N, N, N)
    outcube = np.zeros_like(cube)
    # warmup
    for impl in (single_threaded, parallelized):
        impl(cube[0])

    for impl in (single_threaded, parallelized):
        start = time.time()
        for i in range(N):
            outcube[i] = impl(cube[i])
        print(f"Time per iteration: {(time.time() - start) / N}  {impl}")

if __name__ == "__main__":
    import sys
    try:
        N = int(sys.argv[1])
    except (ValueError, IndexError):
        N = 16
    main(N)