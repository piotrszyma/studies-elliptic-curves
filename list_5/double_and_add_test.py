import collections
import unittest
import random

import double_and_add
import setup

import affine
import projective
import field
import jacobi
from shared import CurveBasePoint, CurveParams

AffinePoint = affine.AffinePoint
ProjectivePoint = projective.ProjectivePoint
FieldInt = field.FieldInt
JacobiPoint = jacobi.JacobiPoint


def _setup_curve():
    curve_params = CurveParams(
        base_point=CurveBasePoint(x=247845205144, y=706036928873, z=1),
        a=479578361930,
        b=77472502557,
        curve_order=846154605337,
        field_order=846155904851,
    )
    affine.set_curve_params(curve_params)
    projective.set_curve_params(curve_params)
    jacobi.set_curve_params(curve_params)
    field.set_modulus(curve_params.field_order)


class DoubleAndAddTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _setup_curve()

    def test_on_projective(self):
        # Arrange.
        for _ in range(100):
            k = random.getrandbits(40)
            with self.subTest(k):
                base_point = ProjectivePoint.base()
                expected_result = base_point * k

                # Act.
                result = double_and_add.double_and_add(base_point, k)

                # Assert.
                self.assertEqual(expected_result, result)

    def test_on_jacobi(self):
        # Arrange.
        # for _ in range(100):
        k = random.getrandbits(40)
        # with self.subTest(k):
        expected_result = AffinePoint.base() * k
        base_point = JacobiPoint.base()

        # Act.
        result = double_and_add.double_and_add(base_point, k)

        # Assert.
        self.assertEqual(expected_result, result.convert_to_affine_point())


if __name__ == "__main__":
    unittest.main()
