import time
import random
import threading

timers = {}

def timer():
    def inner(func):
        def arg_handler(*args):
            t = time.time()
            timers.setdefault(func.__name__,[])
            res = func(*args)
            timers[func.__name__].append(time.time() - t)
            return res
        return arg_handler
    return inner


@timer()
def bubble(arr:list) -> list:

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


@timer()
def replacer(arr:list) -> list:
    for i in range(len(arr)):
        target = arr[i]

        while (i-1 >= 0 and target < arr[i-1]):
            arr[i] = arr[i-1]
            i -= 1
        arr[i] = target

    return arr


@timer()
def selection(arr:list) -> list:
    for i in range(0, len(arr) - 1):
        smallest = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[smallest]:
                smallest = j
        arr[i], arr[smallest] = arr[smallest], arr[i]

    return arr


@timer()
def insertion_binary(arr:list) -> list:
    for i in range(len(arr)):
        key = arr[i]
        lo, hi = 0, i - 1
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if key < arr[mid]:
                hi = mid
            else:
                lo = mid + 1
        for j in range(i, lo + 1, -1):
            arr[j] = arr[j - 1]
        arr[lo] = key
    return arr


def get_test_arr(limit:int, _range:int) -> list:
    return [random.randint(-limit, limit) for i in range(_range)]


@timer()
def test_function(i:int):
    test_array = get_test_arr(2000, 1000)
    s = sorted(test_array)

    assert s == bubble(test_array), f'Bubble sort ERROR {i} :('
    assert s == selection(test_array), f'Selection sort ERROR {i} :('
    assert s == replacer(test_array), f'replacer sort ERROR {i} :('
    assert s == insertion_binary(test_array), f'insertion_binary sort ERROR {i} :('
    print(f'Complete: {i}')


def test_func_starter():
    threads = []
    
    for i in range(100):
        t = threading.Thread(target=test_function, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == '__main__':

    test_func_starter()

    for func in timers:
        print(f"Total time in {func}: {sum(timers[func])/len(timers[func])} | MIN: {min(timers[func])} | MAX {max(timers[func])}")

