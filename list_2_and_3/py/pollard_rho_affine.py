import dataclasses
import random
import copy
import math
from typing import Tuple, Optional

import timer
import affine


@dataclasses.dataclass
class EcAffinePollardRhoDLParams:
    base_point: affine.AffinePoint
    mul_point: affine.AffinePoint
    field_order: int
    curve_order: int

    def __str__(self):
        return (
            f"EcAffinePollardRhoDLParams"
            f"(base_point={self.base_point}, q_point={self.q_point})"
        )


@dataclasses.dataclass
class Coeffs:
    alpha: int = 0
    beta: int = 0


def generate_params(curve_params: affine.CurveParams) -> EcAffinePollardRhoDLParams:
    base_point = affine.AffinePoint(
        curve_params.base_point.x, curve_params.base_point.y
    )

    k = random.randint(2, curve_params.curve_order)

    mul_result = k * base_point
    return EcAffinePollardRhoDLParams(
        base_point=base_point,
        mul_point=mul_result,
        field_order=curve_params.field_order,
        curve_order=curve_params.curve_order,
    )


def _in_s1(point: affine.AffinePoint):
    return point.x % 3 == 1


def _in_s2(point: affine.AffinePoint):
    return point.x % 3 == 0


def _in_s3(point: affine.AffinePoint):
    return point.x % 3 == 2


def modinv(a, n):
    b, c = 1, 0
    while n:
        q, r = divmod(a, n)
        a, b, c, n = n, c, b - q * c, r
    # at this point a is the gcd of the original inputs
    if a == 1:
        return b
    raise ValueError(f"{a} is not invertible modulo {n}")


class EcAffinePollardRhoDL:
    def __init__(self, params: EcAffinePollardRhoDLParams):
        self.base_point: affine.AffinePoint = params.base_point
        self.mul_point: affine.AffinePoint = params.mul_point
        self.field_order: int = params.field_order
        self.curve_order: int = params.curve_order

    def _f(self, values: Tuple[affine.AffinePoint, Coeffs]) -> Tuple[int, Coeffs]:
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
        betas_inv = modinv(betas_diff, self.curve_order)

        result = (alphas_diff * betas_inv) % self.curve_order

        # found_mul = (slow_coeffs.alpha - fast_coeffs.alpha) // (
        #     fast_coeffs.beta - slow_coeffs.beta
        # )
        # Return found_mul being ECDL such that base_pount * found_mul = mul_point
        return result

    def run(self):
        return self._walk()


def main():
    pass
    # curve_params = affine.CurveParams(
    #     base_point=affine.CurveBasePoint(172235452673, 488838007757),
    #     a=236367012452,
    #     b=74315650609,
    #     field_order=807368793739,
    #     curve_order=807369655039,
    # )
    # params = generate_params(curve_params)
    # print(f"Running for {curve_params}")
    # instance = EcAffinePollardRhoDL(params)

    # with timer.timeit("PollardRhoDL algorithm"):
    #     x_found = instance.run()

    # print(f"x_found: {x_found}")

    # real = params.y
    # restored = pow(params.g_prim, x_found, params.p)

    # print(f"Real: g_prim^x = {real}, restored: g_prim^x_found {restored}")


if __name__ == "__main__":
    main()
