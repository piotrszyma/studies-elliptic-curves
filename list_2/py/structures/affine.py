import collections
import random
import copy
import math
import dataclasses

from typing import Optional

CurveBasePoint = collections.namedtuple("CurveBasePoint", "x y")


@dataclasses.dataclass
class CurveParams:
    base_point: CurveBasePoint
    a: int
    b: int
    curve_order: int
    field_order: int


_CURVE_PARAM_ORDER = 807369655039
_CURVE_PARAM_FIELD_ORDER = 807368793739
_CURVE_PARAM_A = 236367012452
_CURVE_PARAM_B = 74315650609
_CURVE_PARAM_BASE_POINT = CurveBasePoint(172235452673, 488838007757)


def set_curve_params(curve_params: CurveParams):
    global _CURVE_PARAM_BASE_POINT
    global _CURVE_PARAM_ORDER
    global _CURVE_PARAM_FIELD_ORDER
    global _CURVE_PARAM_A
    global _CURVE_PARAM_B
    _CURVE_PARAM_BASE_POINT = curve_params.base_point
    _CURVE_PARAM_ORDER = curve_params.curve_order
    _CURVE_PARAM_FIELD_ORDER = curve_params.field_order
    _CURVE_PARAM_A = curve_params.a
    _CURVE_PARAM_B = curve_params.b


def modinv(a, n):
    b, c = 1, 0
    while n:
        q, r = divmod(a, n)
        a, b, c, n = n, c, b - q * c, r
    # at this point a is the gcd of the original inputs
    if a == 1:
        return b
    raise ValueError("Not invertible")


class AffinePoint:
    _inf = None
    _base_point = None
    __slots__ = ("x", "y")

    def __init__(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        inf: Optional[bool] = False,
    ):
        self.x = x % _CURVE_PARAM_FIELD_ORDER if x else x
        self.y = y % _CURVE_PARAM_FIELD_ORDER if y else y

    def __repr__(self):
        if self.is_infinity():
            return "AffinePoint(at infinity)"
        return f"AffinePoint({self.x}, {self.y})"

    def __eq__(self, other: "AffinePoint") -> bool:
        if not isinstance(other, AffinePoint):
            return False

        if self.is_infinity() and other.is_infinity():
            return True

        return self.x == other.x and self.y == other.y

    def __mul__(self, value: int) -> "AffinePoint":
        if not isinstance(value, int):
            raise NotImplementedError(f"Cannot multiply {type(self)} and {type(value)}")

        value = value % _CURVE_PARAM_ORDER

        if value == 2:
            if self.is_infinity():
                return self.get_infinity()

            if self.y == 0:
                return self.get_infinity()

            s = (
                pow(self.x, 2, _CURVE_PARAM_FIELD_ORDER) * 3 + _CURVE_PARAM_A
            ) * modinv(2 * self.y, _CURVE_PARAM_FIELD_ORDER)
            x2 = pow(s, 2, _CURVE_PARAM_FIELD_ORDER) - 2 * self.x
            y2 = (s * (self.x - x2)) - self.y

            return AffinePoint(x=x2, y=y2)

        temp = copy.deepcopy(self)
        result = AffinePoint.get_infinity()

        while value != 0:
            if value & 1 != 0:
                result += temp
            temp *= 2
            value >>= 1

        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other: "AffinePoint") -> "AffinePoint":
        if not isinstance(other, AffinePoint):
            raise NotImplementedError(f"Cannot multiply {type(self)} and {type(other)}")

        if self.is_infinity():
            return other

        if other.is_infinity():
            return self

        if self.x == other.x:
            if self.y == other.y:
                return self * 2
            return AffinePoint.get_infinity()

        s = (self.y - other.y) * modinv(self.x - other.x, _CURVE_PARAM_FIELD_ORDER)

        x_ = s ** 2 - self.x - other.x
        y_ = s * (self.x - x_) - self.y

        return AffinePoint(x=x_, y=y_)

    def __radd__(self, other):
        return self.__add__(other)

    def is_infinity(self):
        return self.x is None and self.y is None

    @classmethod
    def random(cls):
        return cls.get_base_point() * random.randint(2, _CURVE_PARAM_ORDER)

    @classmethod
    def get_infinity(cls):
        if cls._inf:
            return cls._inf
        cls._inf = cls()
        return cls._inf

    @classmethod
    def get_base_point(cls):
        if cls._base_point:
            return cls._base_point
        cls._base_point = cls(*_CURVE_PARAM_BASE_POINT)
        return cls._base_point
