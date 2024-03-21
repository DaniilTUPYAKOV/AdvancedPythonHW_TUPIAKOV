import math
import concurrent.futures
import time
from multiprocessing import cpu_count


class TimeComparator:

    _runner_names: set[str] = set()
    _data: dict[int, dict[str, int]] = {}

    def add_timestamp(self, runner_name: str, runner_settings: int, result_time: int):
        if runner_settings not in self._data:
            self._data[runner_settings] = {}
        self._data[runner_settings][runner_name] = result_time
        self._runner_names.add(runner_name)

    def __str__(self) -> str:
        tab = len(str(max(self._data.keys()))) + 3
        start = f"{' '*(tab - 4)}jobs"
        for elem in self._runner_names:
            start += "   " + elem
        result = [start]
        for settings, data_dict in self._data.items():
            temp = f"{' '*(tab - len(str(settings)))}{str(settings)}"
            for elem in self._runner_names:
                temp += (
                    "   "
                    + f"{' '*(len(elem)-len(str(data_dict[elem]))-8)}"
                    + str(data_dict[elem])
                    + " seconds"
                )
            result.append(temp)
        return "\n".join(result)


TIME_COMPARATOR = TimeComparator()


def save_log(log: str, filename: str):
    with open(filename, "a+", encoding="utf-8") as file:
        file.write(log + "\n")


def integrate_thread(f, a, b, *, n_jobs=1, n_iter=10000000):

    step = (b - a) / n_iter
    indices = [
        (i * (n_iter // n_jobs), (i + 1) * (n_iter // n_jobs)) for i in range(n_jobs)
    ]

    def integrate_range_thread(start, end):
        acc = 0
        for i in range(start, end):
            acc += f(a + i * step) * step
        return acc

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = [
            executor.submit(integrate_range_thread, start, end)
            for start, end in indices
        ]
        return sum(
            future.result() for future in concurrent.futures.as_completed(futures)
        )


def integrate_range_process(task: tuple):
    start = task[0]
    end = task[1]
    main_start = task[2]
    step = task[3]
    f = task[4]
    acc = 0
    for i in range(start, end):
        acc += f(main_start + i * step) * step
    return acc


def integrate_process(f, a, b, *, n_jobs=1, n_iter=10000000):

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        step = (b - a) / n_iter
        tasks = [
            (i * (n_iter // n_jobs), (i + 1) * (n_iter // n_jobs), a, step, f)
            for i in range(n_jobs)
        ]
        results = executor.map(integrate_range_process, tasks)
        result = sum(results)

    return result


def run_integration(f, a, b, executor_class, n_jobs):

    save_log(
        f"Starting integration with {executor_class.__name__} and n_jobs={n_jobs}, start time = {time.time()}",
        "log.txt",
    )

    start_time = time.time()

    if executor_class == concurrent.futures.ThreadPoolExecutor:
        result = integrate_thread(f, a, b, n_jobs=n_jobs)
    else:
        result = integrate_process(f, a, b, n_jobs=n_jobs)

    end_time = time.time()

    TIME_COMPARATOR.add_timestamp(
        executor_class.__name__, n_jobs, round(end_time - start_time, 3)
    )

    return result


if __name__ == "__main__":
    n_iter = 10000000
    cpu_num = cpu_count()
    open("log.txt", "w", encoding="utf-8").close()
    for executor_class in [
        concurrent.futures.ThreadPoolExecutor,
        concurrent.futures.ProcessPoolExecutor,
    ]:
        for n_jobs in range(1, cpu_num * 2 + 1):
            run_integration(math.cos, 0, math.pi / 2, executor_class, n_jobs)

    with open("compare_times.txt", "w", encoding="utf-8") as file:
        file.write(str(TIME_COMPARATOR))
