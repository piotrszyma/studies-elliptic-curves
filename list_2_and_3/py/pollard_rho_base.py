import dataclasses
import copy
import math

from typing import Tuple, Any

import shared

Point = Any


@dataclasses.dataclass
class Coeffs:
    alpha: int = 0
    beta: int = 0


def _in_s1(point: Point):
    return point.x % 3 == 1


def _in_s2(point: Point):
    return point.x % 3 == 0


def _in_s3(point: Point):
    return point.x % 3 == 2


class AbstractEcPollardRhoDL:
    def _f(self, values: Tuple[Point, Coeffs]) -> Tuple[int, Coeffs]:
        value, coeffs = values
        if _in_s1(value):
            coeffs.alpha += 1
            coeffs.alpha %= self.curve_order
            return value + self.base_point, coeffs
        elif _in_s2(value):
            coeffs.alpha *= 2
            coeffs.alpha %= self.curve_order
            coeffs.beta *= 2
            coeffs.beta %= self.curve_order
            return value * 2, coeffs
        elif _in_s3(value):
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

        while True:

            slow, slow_coeffs = self._f((slow, slow_coeffs))
            fast, fast_coeffs = self._f(self._f((fast, fast_coeffs)))

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
