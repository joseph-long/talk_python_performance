import ray
import time
import random

@ray.remote
def time_waster(min_delay: float = 1, max_delay: float = 10) -> float:
    delay = (max_delay - min_delay) * random.random() + min_delay
    time.sleep(delay)
    return delay

def main():
    ray.init()
    pending_results = []
    for _ in range(10):
        ref = time_waster.remote(min_delay=2, max_delay=3)
        pending_results.append(ref)
    for ref in pending_results:
        result = ray.get(ref)
        print(f"Delay was {result} sec")

if __name__ == "__main__":
    start = time.time()
    print(f"Started at {start}")
    main()
    print(f"Took {time.time() - start}")