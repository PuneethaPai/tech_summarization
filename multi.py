import time
from concurrent.futures import ProcessPoolExecutor


def foo3(x, y, size=1000):
    time.sleep(size/1000)
    return [x * y * z for z in range(size)]


def foo2(x, size=100):
    print(x)
    time.sleep(size/1000)
    with ProcessPoolExecutor() as executor:
        return [executor.submit(foo3, x, y).result() for y in range(size)]
    return [foo3(x, y, 1000) for y in range(size)]


def foo1(size=10):
    time.sleep(1 / size)
    return [foo2(x, 100) for x in range(size)]

def square(x: int) -> int:
    time.sleep(.01)
    return x ** 2

def add_n(x: int, n:int = 1) -> int:
    time.sleep(.01)
    return x + 1

def combine(x: int, n: int = 1) -> int:
    return add_n(square(x), n)

if __name__ == "__main__":
    start = time.time()
    initial = range(10000)
    with ProcessPoolExecutor() as executor:
        next = list(executor.map(square, initial))
    with ProcessPoolExecutor() as executor:
        final = [executor.submit(add_n, x, 5) for x in next]
    done = time.time()
    print(f"Done, {start} -> {done} = {done - start}")

    start = done
    with ProcessPoolExecutor() as executor:
        next = list(executor.map(square, initial))
        final = [executor.submit(add_n, x, 5) for x in next]
    done = time.time()
    print(f"Done, {start} -> {done} = {done - start}")

    start = done
    with ProcessPoolExecutor() as executor:
        final = [executor.submit(combine, x, 5) for x in next]
    done = time.time()
    print(f"Done, {start} -> {done} = {done - start}")
