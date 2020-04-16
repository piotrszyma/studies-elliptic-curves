import gensafeprime
import subprocess
import re

RE_PRIME = re.compile(b"prime:\ (?P<value>\d+)")


class FailedToCreatePrimeError:
    pass


if __name__ == "__main__":
    pass
