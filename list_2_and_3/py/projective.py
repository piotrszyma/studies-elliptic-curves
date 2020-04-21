import collections
import random
import copy
import math
import dataclasses

from typing import Optional

CurveBasePoint = collections.namedtuple("CurveBasePoint", "x y z")


@dataclasses.dataclass
class CurveParams:
    base_point: CurveBasePoint
    a: int
    b: int
    curve_order: int
    field_order: int


default_curve_params = CurveParams(
    curve_order=807369655039,
    field_order=807368793739,
    a=236367012452,
    b=74315650609,
    base_point=CurveBasePoint(x=172235452673, y=488838007757, z=1),
)


def set_curve_params(curve_params: CurveParams):
    ProjectivePoint._curve_params = curve_params


def modinv(a, n):
    b, c = 1, 0
    while n:
        q, r = divmod(a, n)
        a, b, c, n = n, c, b - q * c, r
    # at this point a is the gcd of the original inputs
    if a == 1:
        return b
    raise ValueError(f"{a} is not invertible modulo {n}")


class ProjectivePoint:
    _inf = None
    _base_point = None
    _curve_params = default_curve_params
    __slots__ = ("x", "y", "z")

    def __init__(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        z: Optional[int] = None,
        inf: Optional[bool] = False,
    ):
        self.x = x % self._curve_params.field_order if x else x
        self.y = y % self._curve_params.field_order if y else y
        self.z = z % self._curve_params.field_order if z else z

    def __repr__(self):
        if self.is_infinity():
            return "ProjectivePoint(at infinity)"
        return f"ProjectivePoint({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: "ProjectivePoint") -> bool:
        if not isinstance(other, ProjectivePoint):
            return NotImplemented

        if self.is_infinity() and other.is_infinity():
            return True

        return self.x * other.z == other.x * self.z and self.y * other.z == other.y * self.z

    def __ne__(self, other: "ProjectivePoint") -> bool:
        return not (self == other)

    def __mul__(self, value: int) -> "ProjectivePoint":
        if not isinstance(value, int):
            raise NotImplementedError(f"Cannot multiply {type(self)} and {type(value)}")

        value = value % self._curve_params.field_order
        two = 2 % self._curve_params.field_order
        three = 3 % self._curve_params.field_order
        if value == 2:
            if self.is_infinity() or self.y == 0:
                return self.get_infinity()

            t = self.x * self.x * three + self._curve_params.a * self.z * self.z
            u = self.y * self.z * two
            v = u * self.x * self.y * two
            w = t * t - v * two
            x2 = u * w
            y2 = t * (v - w) - u * u * self.y * self.y * two
            z2 = u * u * u

            return ProjectivePoint(x=x2, y=y2, z=z2)

        temp = copy.deepcopy(self)
        result = ProjectivePoint.get_infinity()

        while value != 0:
            if value & 1 != 0:
                result += temp
            temp *= 2
            value >>= 1

        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other: "ProjectivePoint") -> "ProjectivePoint":
        if not isinstance(other, ProjectivePoint):
            raise NotImplementedError(f"Cannot multiply {type(self)} and {type(other)}")

        if self.is_infinity():
            return other

        if other.is_infinity():
            return self

        t0 = self.y * other.z
        t1 = other.y * self.z
        u0 = self.x * other.z
        u1 = other.x * self.z

        if u0 == u1:
            if t0 == t1:
                return self * 2
            else:
                return ProjectivePoint.get_infinity()
        else:
            t = t0 - t1
            u = u0 - u1
            u2 = u * u
            v = self.z * other.z
            w = t * t * v - u2 * (u0 + u1)
            u3 = u * u2
            x_ = u * w
            y_ = t * (u0 * u2 - w) - t0 * u3
            z_ = u3 * v
        return ProjectivePoint(x=x_, y=y_, z=z_)

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        if self.is_infinity():
            return self
        return ProjectivePoint(x=self.x, y=-self.y, z=self.z)

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
        if cls._base_point:
            return cls._base_point
        cls._base_point = cls(*cls._curve_params.base_point)
        return cls._base_point