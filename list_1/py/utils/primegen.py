import gensafeprime
import subprocess
import re

RE_PRIME = re.compile(b"prime:\ (?P<value>\d+)")


class FailedToCreatePrimeError:
    pass


def random_safe_prime_from_gensafeprime(bits: int) -> int:
    assert 40 <= bits <= 64
    return gensafeprime.generate(bits)


def random_safe_prime_from_openssl(bits: int) -> int:
    assert 40 <= bits <= 64
    command = f"openssl dhparam -text {bits}"
    result = subprocess.run(command.split(" "), capture_output=True)

    if result.returncode != 0:
        raise FailedToCreatePrimeError

    return int(RE_PRIME.search(result.stdout).group("value"))


if __name__ == "__main__":
    print(random_safe_prime_from_openssl(5))
