import subprocess
import re

RE_PRIME = re.compile(b"prime:\ (?P<value>\d+)")


class FailedToCreatePrimeError:
    pass


def random_safe_prime(bits=40):
    assert 3 <= bits <= 64
    command = f"openssl dhparam -text {bits}"
    result = subprocess.run(command.split(" "), capture_output=True)

    if result.returncode != 0:
        raise FailedToCreatePrimeError

    return int(RE_PRIME.search(result.stdout).group("value"))
