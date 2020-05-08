import collections
import random
import copy
import math
import dataclasses
from typing import Optional
from field import FieldInt
from shared import CurveParams


def set_curve_params(curve_params: CurveParams):
    AffinePoint._curve_params = curve_params


class AffinePoint:
    _inf = None
    _base_point = None
    _curve_params = None
    __slots__ = ("x", "y")

    def __init__(
        self,
        x: Optional[FieldInt] = None,
        y: Optional[FieldInt] = None,
        inf: Optional[bool] = False,
    ):

        if self._curve_params is None:
            raise RuntimeError("Set AffinePoint curve points first.")

        if x:
            assert y

        if isinstance(x, int):
            x = FieldInt(x)

        if isinstance(y, int):
            y = FieldInt(y)

        self.x = x
        self.y = y

        # if self.x is not None:
        #     self.assert_on_curve()

    def assert_on_curve(self):
        assert (
            self.y * self.y
            == self.x * self.x * self.x
            + self._curve_params.a * self.x
            + self._curve_params.b
        ), f"{self} not on curve."

    def randomness(self):
        return self.x

    def convert_to_projective_point(self):
        from projective import ProjectivePoint

        if self.is_infinity():
            return ProjectivePoint.get_infinity()
        else:
            one = 1 % self._curve_params.field_order
            return ProjectivePoint(self.x, self.y, one)

    def __repr__(self):
        if self.is_infinity():
            return "AffinePoint(at infinity)"
        return f"AffinePoint({self.x}, {self.y})"

    def __eq__(self, other: "AffinePoint") -> bool:
        if not isinstance(other, AffinePoint):
            return NotImplemented

        if self.is_infinity() and other.is_infinity():
            return True

        return self.x == other.x and self.y == other.y

    def __mul__(self, value: int) -> "AffinePoint":
        if not isinstance(value, int):
            raise NotImplementedError(f"Cannot multiply {type(self)} and {type(value)}")

        if value == 2:  # TODO: migrate to Fields
            if self.is_infinity() or self.y == 0:
                return self.get_infinity()

            s = ((self.x ** 2) * 3 + self._curve_params.a) * (2 * self.y).inverse()
            x2 = (s ** 2) - 2 * self.x
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

        s = (self.y - other.y) * (self.x - other.x).inverse()

        x_ = s ** 2 - self.x - other.x
        y_ = s * (self.x - x_) - self.y

        return AffinePoint(x=x_, y=y_)

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        if self.is_infinity():
            return self
        return AffinePoint(x=self.x, y=-self.y)

    def is_infinity(self):
        return self.x is None and self.y is None

    @classmethod
    def random(cls):
        return cls.get_base_point() * random.randint(2, cls._curve_params.curve_order)

    @classmethod
    def get_infinity(cls):
        if cls._inf:
            return cls._inf
        cls._inf = cls()
        return cls._inf

    @classmethod
    def get_base_point(cls):
        import pdb; pdb.set_trace()
        if cls._base_point:
            return cls._base_point
        cls._base_point = cls(*cls._curve_params.base_point)
        return cls._base_point
