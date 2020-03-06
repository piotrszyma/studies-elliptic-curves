import contextlib
import time


@contextlib.contextmanager
def timeit(msg):
    start = time.time()
    try:
        yield
    finally:
        delta = time.time() - start
        print(f"Executed {msg}, it took {delta:.02f} s.")
