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
def shell_sort(arr):
    h = 1
    n = len(arr)
    while h > 0:
            for i in range(h, n):
                c = arr[i]
                j = i
                while j >= h and c < arr[j - h]:
                    arr[j] = arr[j - h]
                    j = j - h
                    arr[j] = c
            h = int(h / 2.2)
    return arr
 
@njit()
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j] :
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = key

@njit()
def selection_sort(array):
    size = len(array)
    for ind in range(size):
        min_index = ind
 
        for j in range(ind + 1, size):
            if array[j] < array[min_index]:
                min_index = j
        array[ind], array[min_index] = array[min_index], array[ind]

@njit()
def bubble_sort(arr):
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

@njit()
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is greater than root
    if l < n and arr[l] > arr[largest]:
        largest = l

    # See if right child of root exists and is greater than largest so far
    if r < n and arr[r] > arr[largest]:
        largest = r

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap

        # Heapify the root.
        heapify(arr, n, largest)

@njit()
def heap_sort(arr):
    n = len(arr)

    # Build a maxheap.
    for i in range(n, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)

@njit()
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        left_half = arr[:mid]  # Dividing the array elements into 2 halves
        right_half = arr[mid:]

        merge_sort(left_half)  # Sorting the first half
        merge_sort(right_half)  # Sorting the second half

        i = j = k = 0

        # Copy data to temporary arrays left_half[] and right_half[]
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

@njit()
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

@njit()
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    stack = [(0, len(arr) - 1)]
    
    while stack:
        low, high = stack.pop()
        pivot_index = partition(arr, low, high)
        
        if pivot_index - 1 > low:
            stack.append((low, pivot_index - 1))
        if pivot_index + 1 < high:
            stack.append((pivot_index + 1, high))
    
    return arr


result = pd.DataFrame(columns=["array_generator", "size", "algorithm", "instruction_count"])
sizes = [10, 100, 1000, 10000, 100000, 1000000]
array_generators = [generate_sorted_array, generate_reversed_sorted_array, generate_random_sorted_array, generate_almost_sorted_array]
algorithms = [shell_sort, insertion_sort, selection_sort, bubble_sort, heap_sort, merge_sort, quick_sort]

for array_generator in array_generators:
    #print(f"{array_generator.__name__}:")
    for size in sizes:
        array = array_generator(size)
        for algorithm in algorithms:
            #print(f"\t{algorithm.__name__}:")
            with Collector() as c:
                algorithm(array)
            
            #print(f"\tSize of {size} take {c.counters.instruction_count} instructions")      
            result = result._append({"array_generator": array_generator.__name__, "size": size, "algorithm": algorithm.__name__, "instruction_count": c.counters.instruction_count}, ignore_index=True)
            print(result)

result.to_csv("result.csv", index=False)
    