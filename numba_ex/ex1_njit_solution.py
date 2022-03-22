import time
import random
import numba
import numpy as np

def demo_implementation(arr):
    width, height = arr.shape
    out = np.zeros_like(arr)
    for i in range(height):
        for j in range(width):
            out[j,i] = random.random()

@numba.jit
def faster(arr):
    width, height = arr.shape
    out = np.zeros_like(arr)
    for i in range(height):
        for j in range(width):
            out[j,i] = random.random()

@numba.njit
def fastest(arr):
    width, height = arr.shape
    out = np.zeros_like(arr)
    for i in range(height):
        for j in range(width):
            out[j,i] = random.random()

def main():
    N = 16
    cube = np.arange(N * N * N, dtype=float).reshape(N, N, N)
    outcube = np.zeros_like(cube)
    # warmup
    for impl in (demo_implementation, faster, fastest):
        impl(cube[0])

    for impl in (demo_implementation, faster, fastest):
        start = time.time()
        for i in range(N):
            outcube[i] = impl(cube[i])
        print(f"Time per iteration: {(time.time() - start) / N}  {impl}")

if __name__ == "__main__":
    main()