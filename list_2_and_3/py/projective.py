from affine import AffinePoint

import collections
import random
import copy
import math
import dataclasses
from typing import Optional
from field import FieldInt

CurveBasePoint = collections.namedtuple("CurveBasePoint", "x y z")


@dataclasses.dataclass
class CurveParams:
    base_point: CurveBasePoint
    a: int
    b: int
    curve_order: int
    field_order: int


def set_curve_params(curve_params: CurveParams):
    ProjectivePoint._curve_params = curve_params


class ProjectivePoint:
    _inf = None
    _base_point = None
    _curve_params = None
    __slots__ = ("x", "y", "z")

    def __init__(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        z: Optional[int] = None,
    ):
        if not self._curve_params:
            raise RuntimeError("Set ProjectivePoint curve params first.")

        if x is None:
            # It is point at infinity.
            self.x, self.y, self.z = None, 1, None
            return

        self.x = FieldInt(x) if not isinstance(x, FieldInt) else x
        self.y = FieldInt(y) if not isinstance(y, FieldInt) else y
        self.z = FieldInt(z) if not isinstance(z, FieldInt) else z

        # if self.y: # TODO: when?
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

    def convert_to_affine_point(self):
        if self.is_infinity():
            return AffinePoint.get_infinity()
        else:
            div = self.z.inverse()
            x = (self.x * div).value % self._curve_params.field_order
            y = (self.y * div).value % self._curve_params.field_order
            return AffinePoint(x, y)

    def __repr__(self):
        if self.is_infinity():
            return f"ProjectivePoint({self.x}, {self.y}, {self.z}) - infinity"
        return f"ProjectivePoint({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: "ProjectivePoint") -> bool:
        if not isinstance(other, ProjectivePoint):
            return NotImplemented

        if self.is_infinity() and other.is_infinity():
            return True

        return (
            self.x * other.z == other.x * self.z
            and self.y * other.z == other.y * self.z
        )

    def __ne__(self, other: "ProjectivePoint") -> bool:
        return not (self == other)

    def __mul__(self, value: FieldInt) -> "ProjectivePoint":
        if isinstance(value, int):
            value = FieldInt(value)

        if not isinstance(value, FieldInt):
            raise NotImplementedError(f"Cannot multiply {type(self)} and {type(value)}")

        two = FieldInt(2)
        three = FieldInt(3)
        a = FieldInt(self._curve_params.a)
        zero = FieldInt(0)

        if value == two:
            if self.is_infinity() or self.y == zero:
                return self.get_infinity()
            t = self.x * self.x * three + a * self.z * self.z
            u = self.y * self.z * two
            v = u * self.x * self.y * two
            w = t * t - v * two

            x2 = u * w
            y2 = t * (v - w) - u * u * self.y * self.y * two
            z2 = u * u * u
            return ProjectivePoint(x=x2, y=y2, z=z2)

        field_value = value
        temp = copy.deepcopy(self)
        result = ProjectivePoint.get_infinity()

        while field_value.value != 0:
            if field_value.value & 1 != 0:
                result += temp
            temp = temp * two
            field_value.value >>= 1

        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other: "ProjectivePoint") -> "ProjectivePoint":
        if not isinstance(other, ProjectivePoint):
            raise NotImplementedError(f"Cannot add {type(self)} and {type(other)}")

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
                return self * FieldInt(2)
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
            # print(f"t: {t}, u: {u}, u2: {u2}, v: {v}, w: {w}, u3: {u3}, x_: {x_}, y_:{y_}, z: {z_}")
        return ProjectivePoint(x=x_, y=y_, z=z_)

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        if self.is_infinity():
            return self
        return ProjectivePoint(x=self.x, y=-self.y, z=self.z)

    def is_infinity(self):
        return self.x is None and self.z is None

    @classmethod
    def random(cls):
        base_point = ProjectivePoint(
            cls.get_base_point().x,
            cls.get_base_point().y,
            cls.get_base_point().z
        )
        random_value = FieldInt(random.randint(2, cls._curve_params.curve_order))
        return base_point * random_value

    @classmethod
    def get_random_number(cls):
        return FieldInt(random.randint(2, cls._curve_params.curve_order))

    @classmethod
    def get_infinity(cls):
        if cls._inf:
            return cls._inf
        cls._inf = cls(None, 1, None)
        return cls._inf

    @classmethod
    def get_base_point(cls):
        if cls._base_point:
            return cls._base_point
        cls._base_point = cls._curve_params.base_point
        return cls._base_point


if __name__ == "__main__":
    import pdb
    import shared
    import field
    base_point = [605600, 205394, 1]
    a = 34328
    b = 354946
    field_order = 649283
    curve_order = 650011
    curve_params = shared.CurveParams(
        base_point=shared.CurveBasePoint(*base_point),
        a=a,
        b=b,
        field_order=field_order,
        curve_order=curve_order,
    )
    field.set_modulus(field_order)
    set_curve_params(curve_params)
