import dataclasses
import copy
import math
import tqdm
import itertools

from typing import Tuple, Any

import shared

Point = Any


@dataclasses.dataclass
class Coeffs:
    alpha: int = 0
    beta: int = 0


class AbstractEcPollardRhoDL:
    def _in_s1(self, value: Point):
        return value.randomness() % 3 == 1

    def _in_s2(self, value: Point):
        return value.randomness() % 3 == 0

    def _in_s3(self, value: Point):
        return value.randomness() % 3 == 2

    def _step(self, value: Point, coeffs: Coeffs, type_: str = None) -> Tuple[int, Coeffs]:
        if self._in_s1(value):
            print(type_, 's1')
            coeffs.alpha += 1
            coeffs.alpha %= self.curve_order
            return value + self.base_point, coeffs
        elif self._in_s2(value):
            print(type_, 's2')
            coeffs.alpha *= 2
            coeffs.alpha %= self.curve_order
            coeffs.beta *= 2
            coeffs.beta %= self.curve_order
            return value * 2, coeffs
        elif self._in_s3(value):
            print(type_, 's3')
            coeffs.beta += 1
            coeffs.beta %= self.curve_order
            return value + self.mul_point, coeffs
        else:
            raise RuntimeError("Impossibru.")

    def _walk(self):
        slow = copy.deepcopy(self.base_point)
        fast = copy.deepcopy(self.base_point)
        slow_coeffs = Coeffs(alpha=1, beta=0)
        fast_coeffs = Coeffs(alpha=1, beta=0)

        for _ in itertools.count():

            slow, slow_coeffs = self._step(slow, slow_coeffs, 's')
            fast, fast_coeffs = self._step(*self._step(fast, fast_coeffs, 'f'), 'f')

            if slow == fast:  # Slow meets fast.
                break

        assert math.gcd(fast_coeffs.beta - slow_coeffs.beta, self.field_order) == 1

        assert (
            slow_coeffs.alpha * self.base_point + slow_coeffs.beta * self.mul_point
            == fast_coeffs.alpha * self.base_point + fast_coeffs.beta * self.mul_point
        )

        alphas_diff = slow_coeffs.alpha - fast_coeffs.alpha
        betas_diff = fast_coeffs.beta - slow_coeffs.beta
        betas_inv = shared.modinv(betas_diff, self.curve_order)
        result = (alphas_diff * betas_inv) % self.curve_order
        return result

    def run(self):
        return self._walk()
