import ray
from tqdm import tqdm
import time
import random

NUMBER_OF_TRIALS = 10
CHUNK_SIZE = 5


def _time_waster(min_delay: float = 1, max_delay: float = 10) -> float:
    delay = (max_delay - min_delay) * random.random() + min_delay
    print(f"Going to sleep for {delay}")
    time.sleep(delay)
    return delay

time_waster = ray.remote(_time_waster)

def main():
    ray.init()
    pending_results = []
    for i in range(NUMBER_OF_TRIALS):
        if i == 0:
            ref = time_waster.remote(min_delay=20, max_delay=30)
        else:
            ref = time_waster.remote(min_delay=2, max_delay=3)
        pending_results.append(ref)
    
    with tqdm(total=len(pending_results)) as pbar:
        while pending_results:
            complete, pending_results = ray.wait(pending_results, timeout=5, num_returns=min(CHUNK_SIZE, len(pending_results)))
            for result in ray.get(complete):
                print(f"Delay was {result} sec")
            if len(complete):
                pbar.update(len(complete))
    

if __name__ == "__main__":
    start = time.time()
    print(f"Started at {start}")
    main()
    print(f"Took {time.time() - start}")