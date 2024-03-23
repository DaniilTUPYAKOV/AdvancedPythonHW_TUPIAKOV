import threading
import multiprocessing
import time

N = 40


def fib(n):
    """ Return n-th Fibonacci number """
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def write_results(method, time):
    """ Write method and time in artifacts file"""
    with open("artifact_4_1.txt", "a+", encoding="utf-8") as file:
        file.write(f"{method} done in {time} seconds\n")


def synchronous_():
    """ Calculate N-th Fibonacci number 10 times and save time """
    start_time = time.time()
    for _ in range(10):
        fib(N)
    end_time = time.time()
    write_results("Synchronous", end_time - start_time)


def threading_():
    """ Calculate N-th Fibonacci number 10 times by 10 Treads and save time"""
    start_time = time.time()
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=fib, args=(N,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    end_time = time.time()
    write_results("Threading", end_time - start_time)


def multiprocessing_():
    """ Calculate N-th Fibonacci number 10 times by 10 processes and save time"""
    processes = []
    start_time = time.time()
    for _ in range(10):
        process = multiprocessing.Process(
            target=fib,
            args=(N,),
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    write_results("Multiprocessing", end_time - start_time)


if __name__ == "__main__":

    open("artifact_4_1.txt", "w", encoding="utf-8").close()

    synchronous_()
    threading_()
    multiprocessing_()
