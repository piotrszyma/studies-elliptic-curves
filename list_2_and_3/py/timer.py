import contextlib
import time


@contextlib.contextmanager
def timeit(msg, time_only=False):
    start = time.time()
    try:
        yield
    finally:
        delta = time.time() - start

        if time_only:
            print(f"{delta:.02f}")
            return

        print(f"Executed {msg}, it took {delta:.02f} s.")
