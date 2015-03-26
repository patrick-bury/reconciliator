from concurrent.futures import ThreadPoolExecutor
import time
def wait_on_b():
    time.sleep(3)
    print("b") # b will never complete because it is waiting on a.
    return 5

def wait_on_a():
    time.sleep(3)
    print("a") # a will never complete because it is waiting on b.
    return 6


executor = ThreadPoolExecutor(max_workers=2)
a = executor.submit(wait_on_b)
b = executor.submit(wait_on_a)