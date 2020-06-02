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
        self.x = FieldInt(x) if x is not None else None
        self.y = FieldInt(y)
        self.z = FieldInt(z) if z is not None else None

    def __repr__(self):
        if self.is_infinity():
            return f"JacobiPoint({self.x}, {self.y}, {self.z}) - infinity"
        return f"JacobiPoint({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: "JacobiPoint") -> bool:
        if not isinstance(other, JacobiPoint):
            return NotImplemented

        return self.x / (self.z ** 2) == other.x / (other.z ** 2) and self.y / (
            self.z ** 3
        ) == other.y / (other.z ** 3)

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __mul__(self, value) -> "JacobiPoint":
        if isinstance(value, int):
            value = FieldInt(value)

        if not isinstance(value, FieldInt):
            return NotImplemented

        if value != 2:
            raise ValueError(f"Only point doubling is supported. ({value} != 2)")

        if self.is_infinity() or self.y.value == 0:
            return self.get_infinity()

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

        if self.is_infinity():
            return other

        if other.is_infinity():
            return self

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

    @classmethod
    def get_infinity(cls):
        return cls(None, 1, None)

    def is_infinity(self):
        return self.x is None and self.z is None

    @classmethod
    def base(cls):
        return cls(
            cls.get_base_point().x, cls.get_base_point().y, cls.get_base_point().z
        )

    @classmethod
    def get_base_point(cls):
        return cls._curve_params.base_point

    def convert_to_affine_point(self):
        return AffinePoint(
            x=self.x * (self.z ** 2).inverse(),
            y=self.y * (self.z ** 3).inverse(),
        )
