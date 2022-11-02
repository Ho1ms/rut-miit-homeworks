import time
import random
import threading

def bubble_sort(arr:list) -> list:

    x = -1
    swapped = True

    while swapped:
        x += 1
        swapped = False

        for i in range(1, len(arr) - x):
            if arr[i - 1] > arr[i]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                swapped = True
    return arr

def get_test_arr(limit:int, _range:int) -> list:
    return [random.randint(-limit, limit) for i in range(_range)]

def test_function(i:int):
    test_array = get_test_arr(2000, 2000)
    assert sorted(test_array) == bubble_sort(test_array), f'Ой, ой, ой! Значение не совпали у {i} :('
    print(f'Complete: {i}')

def test_func_starter():
    for i in range(100):
        threading.Thread(target=test_function, args=(i,)).start()

if __name__ == '__main__':
    t = time.time()

    test_func_starter()

    print(time.time() - t)