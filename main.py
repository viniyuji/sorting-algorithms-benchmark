from random import randint
from cirron import Collector
from numba import njit
import numpy as np

def generate_sorted_array(size: int):
    return np.arange(1, size + 1, 1)

def generate_reversed_sorted_array(size: int):
    return np.arange(size, 0, -1)

def generate_random_sorted_array(size: int):
    return np.random.randint(1, size, size)

def generate_almost_sorted_array(size: int):
    array = np.arange(1, size + 1, 1)

    for _ in range(round(size*0.1)):
        random_index = randint(0, size - 1)
        random_index2 = randint(0, size - 1)
        array[random_index], array[random_index2] = array[random_index2], array[random_index]

    return array

@njit(parallel=True)
def shellSort(nums):
    h = 1
    n = len(nums)
    while h > 0:
            for i in range(h, n):
                c = nums[i]
                j = i
                while j >= h and c < nums[j - h]:
                    nums[j] = nums[j - h]
                    j = j - h
                    nums[j] = c
            h = int(h / 2.2)
    return nums

sizes = [10, 100, 1000, 10000, 100000, 1000000]
array_generators = [generate_sorted_array, generate_reversed_sorted_array, generate_random_sorted_array, generate_almost_sorted_array]

for array_generator in array_generators:
    print(f"{array_generator.__name__}:")
    for size in sizes:
        array = array_generator(size)
        with Collector() as c:
            sorted_array = shellSort(array)
        
        print(f"Size of {size} take {c.counters.instruction_count} instructions")
    