from random import randint
from cirron import Collector
from numba import njit
import numpy as np
import pandas as pd

@njit()
def generate_sorted_array(size: int):
    return np.arange(1, size + 1, 1)

@njit()
def generate_reversed_sorted_array(size: int):
    return np.arange(size, 0, -1)

@njit()
def generate_random_sorted_array(size: int):
    return np.random.randint(1, size, size)

@njit()
def generate_almost_sorted_array(size: int):
    array = np.arange(1, size + 1, 1)

    for _ in range(round(size*0.1)):
        random_index = randint(0, size - 1)
        random_index2 = randint(0, size - 1)
        array[random_index], array[random_index2] = array[random_index2], array[random_index]

    return array

@njit()
def shell_sort(array):
    size = len(array)
    h = 1
    while h > 0:
            for i in range(h, size):
                insert_value = array[i]
                j = i
                while j >= h and insert_value < array[j - h]:
                    array[j] = array[j - h]
                    j = j-h
                array[j] = insert_value
            h //= 2
 
@njit()
def insertion_sort(array):
    for index in range(1, len(array)):
        value = array[index]
        while index > 0 and value < array[index-1]:
                array[index] = array[index-1]
                index -= 1
        array[index] = value

@njit()
def selection_sort(array):
    size = len(array)
    for i in range(size):
        minimum_index = i
 
        for j in range(i + 1, size):
            if array[j] < array[minimum_index]:
                minimum_index = j
        
        if minimum_index != i:
            array[i], array[minimum_index] = array[minimum_index], array[i]

@njit()
def bubble_sort(array):
    size = len(array)

    for i in range(size):
        for j in range(0, size-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]

@njit()
def heapify(array, size, index):
    largest = index
    left_index = 2 * index + 1
    right_index = 2 * index + 2

    if left_index < size and array[left_index] > array[largest]:
        largest = left_index

    if right_index < size and array[right_index] > array[largest]:
        largest = right_index

    if largest != index:
        array[index], array[largest] = array[largest], array[index]
        heapify(array, size, largest)

@njit()
def heap_sort(array):
    size = len(array)

    for i in range(size, -1, -1):
        heapify(array, size, i)

    for i in range(size - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        heapify(array, i, 0)

@njit()
def merge_sort(array):
    if len(array) > 1:
        divisor = len(array) // 2
        left_half = array[:divisor]
        right_half = array[divisor:]

        merge_sort(left_half)
        merge_sort(right_half)

        left_index = right_index = aux_index = 0

        while left_index < len(left_half) and right_index < len(right_half):
            if left_half[left_index] < right_half[right_index]:
                array[aux_index] = left_half[left_index]
                left_index += 1
            else:
                array[aux_index] = right_half[right_index]
                right_index += 1
            aux_index += 1

        while left_index < len(left_half):
            array[aux_index] = left_half[left_index]
            left_index += 1
            aux_index += 1

        while right_index < len(right_half):
            array[aux_index] = right_half[right_index]
            right_index += 1
            aux_index += 1

@njit()
def partition(array, low, high):
    pivot = array[(low + high) // 2]
    i = low - 1
    j = high + 1

    while True:
        i += 1
        while array[i] < pivot:
            i += 1

        j -= 1
        while array[j] > pivot:
            j -= 1

        if i >= j:
            return j

        array[i], array[j] = array[j], array[i]

@njit
def quick_sort(array):
    stack = [(0, len(array) - 1)]
    while stack:
        low, high = stack.pop()
        if low < high:
            p = partition(array, low, high)
            stack.append((low, p))
            stack.append((p + 1, high))


result = pd.DataFrame(columns=["array_generator", "size", "algorithm", "instruction_count"])
sizes = [10, 100, 1000, 10000, 100000, 1000000]
array_generators = [generate_sorted_array, generate_reversed_sorted_array, generate_random_sorted_array, generate_almost_sorted_array]
algorithms = [shell_sort, insertion_sort, selection_sort, bubble_sort, heap_sort, merge_sort, quick_sort]

for array_generator in array_generators:
    for size in sizes:
        array = array_generator(size)
        for algorithm in algorithms:
            with Collector() as c:
                algorithm(array)
            
            result = result._append({"array_generator": array_generator.__name__, "size": size, "algorithm": algorithm.__name__, "instruction_count": c.counters.instruction_count}, ignore_index=True)
            print(result)

result.to_csv("result.csv", index=False)