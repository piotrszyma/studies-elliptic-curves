import collections
import random
import copy
import math

from typing import Optional


CURVE_ORDER = 807369655039
CURVE = "y^2 = x^3 + 236367012452*x + 74315650609"
base_point = collections.namedtuple("base_point", "x y")
CURVE_PARAM_A = 236367012452
CURVE_PARAM_B = 74315650609
CURVE_BASE_POINT = base_point(172235452673, 488838007757)


class AffinePoint:
    _inf = None
    _base_point = None
    __slots__ = ("x", "y")

    def __init__(self, x: Optional[int] = None, y: Optional[int] = None):
        self.x = x
        self.y = y

    def __repr__(self):
        if self.is_infinity():
            return "AffinePoint<at infinity>"
        return f"AffinePoint<{self.x} {self.y}>"

    def __eq__(self, other: "AffinePoint") -> bool:
        if not isinstance(other, AffinePoint):
            return False

        if self.is_infinity() and other.is_infinity():
            return True

        return self.x == other.x and self.y == other.y

    def __mul__(self, value: int) -> "AffinePoint":
        if not isinstance(value, int):
            raise NotImplementedError(f"Cannot multiply {type(self)} and {type(value)}")

        if value == 2:
            if self.is_infinity():
                return self.get_infinity()

            if self.y == 0:
                return self.get_infinity()

            s = (3 * (self.x ** 2) + CURVE_PARAM_A) // (2 * self.y)
            x_ = s ** 2 - 2 * self.x
            y_ = s * (self.x - x_) - self.y
            return AffinePoint(x=x_, y=y_)

        result = copy.deepcopy(self)

        no_muls = math.ceil(math.sqrt(value))
        no_adds = value - 2 ** no_muls

        for _ in range(no_muls):
            result *= 2

        for _ in range(no_adds):
            result += self

        return result

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

        s = (self.y - other.y) // (self.x - other.x)

        x_ = s ** 2 - self.x - other.x
        y_ = s * (self.x - x_) - self.y

        return AffinePoint(x=x_, y=y_)

    def is_infinity(self):
        return self.x is None and self.y is None

    @classmethod
    def random(cls):
        return cls.get_base_point() * random.randint(2, CURVE_ORDER)

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
        cls._base_point = cls(*CURVE_BASE_POINT)
        return cls._base_point
