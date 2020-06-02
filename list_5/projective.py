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
    ProjectivePoint._curve_params = curve_params


class ProjectivePoint:
    _inf = None
    _base_point = None
    _curve_params = None
    __slots__ = ("x", "y", "z")

    def __init__(
        self, x: Optional[int] = None, y: Optional[int] = None, z: Optional[int] = None,
    ):
        if __debug__ and not self._curve_params:
            raise RuntimeError("Set ProjectivePoint curve params first.")

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

    def randomness(self):
        return (self.x * self.z).value

    def coords(self):
        return [self.x.value, self.y.value, self.z.value]

    def convert_to_affine_point(self):
        if self.is_infinity():
            return AffinePoint.get_infinity()
        else:
            div = self.z.inverse()
            x = (self.x * div).value
            y = (self.y * div).value
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

        a = self._curve_params.a

        modulus = self._curve_params.field_order

        if value.value == 2:
            if self.is_infinity() or self.y.value == 0:
                return self.get_infinity()

            # _y_two = self.y * TWO
            # _xx = self.x * self.x
            # _zza = self.z * self.z * FieldInt(a)
            # _xx3 = _xx * THREE
            # _t = _xx3 + _zza
            # _u = self.z * _y_two
            # _v = _u * self.x * _y_two
            # _tt = _t * _t
            # _w = _tt - _v * TWO

            # _uu = _u * _u

            # _x2 = _u * _w
            # _y2 = _t * (_v - _w) - _uu * self.y * self.y * TWO
            # _z2 = _uu * _u
            # return ProjectivePoint(x=_x2, y=_y2, z=_z2)

            y = self.y.value
            x = self.x.value
            z = self.z.value

            y2 = (y * 2) % modulus
            # assert _y_two.value == y2

            zz = (z * z) % modulus
            # assert zz == (self.z * self.z).value

            xx = (x * x) % modulus
            # assert xx == _xx.value

            xx3 = (xx * 3) % modulus
            # assert xx3 == (self.x * self.x * THREE).value

            zza = (zz * a) % modulus

            # assert zza == _zza.value

            t = (xx3 + zza) % modulus
            # assert _t.value == t

            u = (z * y2) % modulus

            # assert _u.value == u

            ux = u * x % modulus

            v = ux * y2 % modulus

            tt = (t * t) % modulus
            # assert _tt.value == tt

            v2 = v * 2 % modulus

            w = (tt - v2) % modulus
            # assert _w.value == w

            uu = (u * u) % modulus

            x2 = u * w % modulus

            yy = y * y % modulus

            v_w = (v - w) % modulus
            uuyy = uu * yy % modulus
            uuyy2 = uuyy * 2 % modulus

            tv_w = t * v_w % modulus

            y2 = (tv_w - uuyy2) % modulus

            z2 = uu * u % modulus
            # assert _x2.value == x2
            # assert _y2.value == y2
            # assert _z2.value == z2
            return ProjectivePoint(x=x2, y=y2, z=z2)

        TWO = FieldInt(2)
        field_value = value
        temp = copy.deepcopy(self)
        result = ProjectivePoint.get_infinity()

        while field_value.value != 0:
            if field_value.value & 1 != 0:
                result += temp
            temp = temp * TWO
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

        modulus = self._curve_params.field_order

        t0 = (self.y.value * other.z.value) % modulus
        # _t0 = self.y * other.z
        # assert t0 == _t0.value

        t1 = other.y.value * self.z.value % modulus
        # _t1 = other.y * self.z
        # assert t1 == _t1.value

        u0 = self.x.value * other.z.value % modulus
        # _u0 = self.x * other.z
        # assert _u0.value == u0

        u1 = other.x.value * self.z.value % modulus
        # _u1 = other.x * self.z
        # assert _u1.value == u1

        if u0 == u1:
            if t0 == t1:
                return self * FieldInt(2)
            else:
                return ProjectivePoint.get_infinity()
        else:

            s_z = self.z.value
            # _s_z = self.z

            o_z = other.z.value
            # _o_z = other.z

            t = (t0 - t1) % modulus
            # _t = _t0 - _t1
            # assert _t.value == t

            u0m1 = (u0 - u1) % modulus
            # _u0m1 = _u0 - _u1
            # assert _u0m1.value == u0m1

            u0p1 = (u0 + u1) % modulus
            # _u0p1 = _u0 + _u1
            # assert _u0p1.value == u0p1

            u2 = u0m1 * u0m1 % modulus
            # _u2 = _u0m1 * _u0m1
            # assert _u2.value == u2

            v = s_z * o_z % modulus
            # _v = _s_z * _o_z
            # assert _v.value == v

            tt = t * t % modulus
            # _tt = _t * _t
            # assert _tt.value == tt

            ttv = tt * v % modulus
            # _ttv = _tt * _v
            # assert _ttv.value == ttv

            u2_u0p1 = u2 * u0p1 % modulus
            # _u2_u0p1 = _u2 * (_u0p1)
            # assert _u2_u0p1.value == u2_u0p1

            w = (ttv - u2_u0p1) % modulus
            # _w = _ttv - _u2_u0p1
            # assert _w.value == w

            u3 = u0m1 * u2 % modulus
            # _u3 = _u0m1 * _u2

            x = u0m1 * w
            # x_ = _u0m1 * _w

            u0_u2 = u0 * u2 % modulus
            # _u0_u2 = _u0 * _u2

            u0_u2_m_w = (u0_u2 - w) % modulus
            # _u0_u2_m_w = _u0_u2 - _w
            # assert _u0_u2_m_w.value == u0_u2_m_w

            # _t_u0_u2_m_w = _t * _u0_u2_m_w
            t_u0_u2_m_w = t * u0_u2_m_w

            # _t0_u3 = _t0 * _u3
            t0_u3 = t0 * u3 % modulus

            y = (t_u0_u2_m_w - t0_u3) % modulus
            # y_ = _t_u0_u2_m_w - _t0_u3
            # assert y_.value == y

            z = u3 * v % modulus
            # z_ = _u3 * _v
            # assert z_.value == z

        return ProjectivePoint(x=x, y=y, z=z)

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        if self.is_infinity():
            return self
        return ProjectivePoint(x=self.x.value, y=-self.y.value, z=self.z.value)

    def is_infinity(self):
        return self.x is None and self.z is None

    @classmethod
    def random(cls):
        base_point = ProjectivePoint(
            cls.get_base_point().x, cls.get_base_point().y, cls.get_base_point().z
        )
        random_value = FieldInt(random.randint(2, cls._curve_params.curve_order))
        return base_point * random_value

    @classmethod
    def base(cls):
        return ProjectivePoint(
            cls.get_base_point().x, cls.get_base_point().y, cls.get_base_point().z
        )

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
        return cls._curve_params.base_point


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
