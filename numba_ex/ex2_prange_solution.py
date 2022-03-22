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

@numba.njit(parallel=True)
def nested_threads(arr):
    width, height = arr.shape
    out = np.zeros_like(arr)
    for i in numba.prange(height):
        for j in numba.prange(width):
            out[j,i] = random.random()

@numba.njit(parallel=True)
def top_level_parallelism(cube):
    planes, width, height = cube.shape
    outcube = np.zeros_like(cube)
    for p in numba.prange(planes):
        for i in range(height):
            for j in range(width):
                outcube[p, j, i] = random.random()
    return outcube

def main(N):
    cube = np.arange(N * N * N, dtype=float).reshape(N, N, N)
    outcube = np.zeros_like(cube)
    # warmup
    for impl in (single_threaded, nested_threads):
        impl(cube[0])
    top_level_parallelism(cube)

    for impl in (single_threaded, nested_threads):
        start = time.time()
        for i in range(N):
            outcube[i] = impl(cube[i])
        print(f"Time per iteration: {(time.time() - start) / N}  {impl}")
    
    start = time.time()
    top_level_parallelism(cube)
    print(f"Time per iteration: {(time.time() - start) / N}  {top_level_parallelism}")

if __name__ == "__main__":
    import sys
    try:
        N = int(sys.argv[1])
    except ValueError:
        N = 16
    main(N)