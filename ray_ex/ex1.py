import time
import random
import ray

@ray.remote
def time_waster(min_delay: float = 1, max_delay: float = 10) -> float:
    delay = (max_delay - min_delay) * random.random() + min_delay
    time.sleep(delay)
    return delay

def main():
    pending = []
    for i in range(10):
        if i == 0:
            ref = time_waster.remote(min_delay=20, max_delay=30)
        else:
            ref = time_waster.remote(min_delay=2, max_delay=3)
        print(ref)
        pending.append(ref)
        print('submitted', i)
    for ref in pending:
        print("About to get")
        result = ray.get(ref)
        print("Got!")
        print(f"Delay was {result} sec")

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Took {time.time() - start}")