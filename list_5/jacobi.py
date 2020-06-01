from affine import AffinePoint

import collections
import random
import copy
import dataclasses
from typing import Optional
from field import FieldInt, MODULUS

CurveBasePoint = collections.namedtuple("CurveBasePoint", "x y z")


@dataclasses.dataclass
class CurveParams:
    base_point: CurveBasePoint
    a: int
    b: int
    curve_order: int
    field_order: int


def set_curve_params(curve_params: CurveParams):
    JacobiPoint._curve_params = curve_params


class JacobiPoint:
    _inf = None
    _base_point = None
    _curve_params = None
    __slots__ = ("x", "y", "z")

    def __init__(
        self, x: Optional[int] = None, y: Optional[int] = None, z: Optional[int] = None,
    ):
        if __debug__ and not self._curve_params:
            raise RuntimeError("Set JacobiPoint curve params first.")

        if x is None:
            # It is point at infinity.
            self.x, self.y, self.z = None, FieldInt(1), None
            return

        self.x = FieldInt(x)
        self.y = FieldInt(y)
        self.z = FieldInt(z)

        if __debug__:
            self.assert_on_curve()

    def assert_on_curve(self):
        if self.is_infinity():
            return True

        assert (
            self.y * self.y * self.z
            == self.x * self.x * self.x
            + self._curve_params.a * self.x * self.z * self.z
            + self._curve_params.b * self.z * self.z * self.z
        ), f"{self} is not on curve."

    def __repr__(self):
        if self.is_infinity():
            return f"JacobiPoint({self.x}, {self.y}, {self.z}) - infinity"
        return f"JacobiPoint({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: "JacobiPoint") -> bool:
        if not isinstance(other, JacobiPoint):
            return NotImplemented

        if self.is_infinity() and other.is_infinity():
            return True

        return (
            self.x * other.z == other.x * self.z
            and self.y * other.z == other.y * self.z
        )

    def __ne__(self, other: "JacobiPoint") -> bool:
        return not (self == other)

    def __mul__(self, value: FieldInt) -> "JacobiPoint":
        if isinstance(value, int):
            value = FieldInt(value)

        if not isinstance(value, FieldInt):
            return NotImplemented

        X_1 = self.x
        Y_1 = self.y
        Z_1 = self.z

        M = 3 * X_1 * X_1 + self._curve_params.a * Z_1 * Z_1 * Z_1 * Z_1
        Z_2 = 2 * Y_1 * Z_1
        S = 4 * X_1 * Y_1 * Y_1
        X_2 = M * M - 2 * S
        T = 8 * Y_1 * Y_1 * Y_1 * Y_1
        Y_2 = M * (S - X_2) - T

        return JacobiPoint(x=X_2, y=Y_2, z=Z_2)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other: "JacobiPoint") -> "JacobiPoint":
        if not isinstance(other, JacobiPoint):
            return NotImplemented

        X_0 = self.x
        Y_0 = self.y
        Z_0 = self.z

        X_1 = other.x
        Y_1 = other.y
        Z_1 = other.z

        U_0 = X_0 * Z_1 * Z_1
        S_0 = Y_0 * Z_1 * Z_1 * Z_1
        U_1 = X_1 * Z_0 * Z_0
        S_1 = Y_1 * Z_0 * Z_0 * Z_0

        W = U_0 - U_1
        R = S_0 - S_1
        T = U_0 + U_1
        M = S_0 + S_1

        Z_2 = W * Z_0 * Z_1
        X_2 = R * R - T * W * W
        V = T * W * W - 2 * X_2
        Y_2 = (V * R - M * W * W * W) * FieldInt(2).inverse()

        return JacobiPoint(x=X_2, y=Y_2, z=Z_2)

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        if self.is_infinity():
            return self
        return JacobiPoint(x=self.x.value, y=-self.y.value, z=self.z.value)

    def is_infinity(self):
        return self.x is None and self.z is None

    @classmethod
    def get_infinity(cls):
        if cls._inf:
            return cls._inf
        cls._inf = cls(None, 1, None)
        return cls._inf

    @classmethod
    def get_base_point(cls):
        # if cls._base_point:
        # return cls._base_point
        cls._base_point = cls._curve_params.base_point
        return cls._base_point


if __name__ == "__main__":
    import argparse
    import affine
    import setup

    parser = argparse.ArgumentParser()
    parser.add_argument("--gx", type=int, required=True, help="x of base Point")
    parser.add_argument("--gy", type=int, required=True, help="y of base Point")
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--stdin", action="store_true", default=False)
    parser.add_argument(
        "--R", type=int, required=True, help="Value by which to multiply affine point"
    )
    args = parser.parse_args()
    setup.set_curve_params(args)

    base = affine.AffinePoint(args.gx, args.gy).convert_to_projective_point()
    exp = args.R
    result = base * exp
