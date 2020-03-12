import dataclasses
import random

from typing import Tuple

from utils import primegen
from utils import timer


@dataclasses.dataclass
class PollardRhoDLParams:
    g_prim: int
    p: int
    p_prim: int
    y: int

    def __str__(self):
        return f"g_prim: {self.g_prim}, p: {self.p}, p_prim: {self.p_prim}, y: {self.y}"


@dataclasses.dataclass
class Point:
    alpha: int = 0
    beta: int = 0


def generate_params(bits: int = 40) -> PollardRhoDLParams:
    p = primegen.random_safe_prime_openssl(bits)

    p_prim = (p - 1) // 2

    g = random.randint(2, p - 1)
    g_prim = pow(g, 2, p)

    rn = random.randint(2, p - 1)
    y = pow(rn, 2, p)  # To make QR.
    return PollardRhoDLParams(g_prim=g_prim, p=p, p_prim=p_prim, y=y,)


def _in_s1(e: int):
    return e % 3 == 1


def _in_s2(e: int):
    return e % 3 == 0


def _in_s3(e: int):
    return e % 3 == 2


class PollardRhoDL:
    def __init__(self, params: PollardRhoDLParams):
        self.params = params

    def _f(self, values: Tuple[int, Point]) -> Tuple[int, Point]:
        value, poe = values
        if _in_s1(value):
            poe.beta += 1
            return (value * self.params.y) % self.params.p, poe
        elif _in_s2(value):
            poe.alpha *= 2
            poe.beta *= 2
            return (value * value) % self.params.p, poe
        elif _in_s3(value):
            poe.alpha += 1
            return (self.params.g_prim * value) % self.params.p, poe
        else:
            raise RuntimeError("Impossibru.")

    def _walk(self):
        A = 1
        B = 1
        poeA = Point()
        poeB = Point()

        while True:

            A, poeA = self._f((A, poeA))
            B, poeB = self._f(self._f((B, poeB)))

            if A == B:
                break

        b_invs = pow(poeA.beta - poeB.beta, self.params.p_prim - 2, self.params.p_prim)
        a_deltas = poeB.alpha - poeA.alpha

        return a_deltas * b_invs % self.params.p_prim

    def run(self):
        return self._walk()


def main():
    params = generate_params()
    print(f"Running for {params}")

    instance = PollardRhoDL(params)

    with timer.timeit("PollardRhoDL algorithm"):
        x_found = instance.run()

    print(f"x_found: {x_found}")

    real = params.y
    restored = pow(params.g_prim, x_found, params.p)

    print(f"Real: g_prim^x = {real}, restored: g_prim^x_found {restored}")


if __name__ == "__main__":
    main()
