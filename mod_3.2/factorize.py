from multiprocessing import Pool, cpu_count
import time


def factorize_one_process(*numbers):
    result = []
    for number in numbers:
        dividers = []
        for i in range(1, int(number / 2) + 1):
            if number % i == 0:
                dividers.append(i)
        dividers.append(number)
        result.append(dividers)
    return result


def factorize_multy_process(number):
    dividers = []
    for i in range(1, int(number / 2) + 1):
        if number % i == 0:
            dividers.append(i)
    dividers.append(number)
    return dividers


if __name__ == '__main__':
    start = time.time()
    a, b, c, d = factorize_one_process(128, 255, 99999, 10651060)
    speed = time.time() - start
    print(f"One process speed: {speed}")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    start = time.time()
    with Pool(processes=cpu_count()) as pool:
        a, b, c, d = pool.map(factorize_multy_process, (128, 255, 99999, 10651060))
        assert a == [1, 2, 4, 8, 16, 32, 64, 128]
        assert b == [1, 3, 5, 15, 17, 51, 85, 255]
        assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
        assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                     1521580, 2130212, 2662765, 5325530, 10651060]

    speed = time.time() - start
    print(f"Eight processes speed: {speed}")


