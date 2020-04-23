import unittest
import unittest.mock as mock
import random

import pollard_rho_affine as affine_rho
import pollard_rho_projective as projective_rho

import field
import projective
import affine
import shared


class TestRhoPollard(unittest.TestCase):
    @mock.patch.object(random, "randint", new=lambda *args: 2)
    def test_run_affine(self):
        # Arrange.
        curve_params = shared.CurveParams(
            base_point=shared.CurveBasePoint(2928, 42354),
            a=40798,
            b=14047,
            field_order=62071,
            curve_order=62039,
        )
        # curve_params = shared.CurveParams(
        #     base_point=shared.CurveBasePoint(172235452673, 488838007757),
        #     a=236367012452,
        #     b=74315650609,
        #     field_order=807368793739,
        #     curve_order=807369655039,
        # )
        # curve_params = shared.CurveParams(
        #     base_point=shared.CurveBasePoint(x=149291979771, y=473920439653),
        #     a=370440899758,
        #     b=287897364263,
        #     curve_order=569718564161,
        #     field_order=569719867697,
        # )

        field.set_modulus(curve_params.field_order)

        X = field.FieldInt(curve_params.base_point.x)
        Y = field.FieldInt(curve_params.base_point.y)
        A = field.FieldInt(curve_params.a)
        B = field.FieldInt(curve_params.b)

        assert Y * Y == X * X * X + A * X + B
        affine.set_curve_params(curve_params)
        params = affine_rho.generate_params(curve_params)
        instance = affine_rho.EcAffinePollardRhoDL(params)

        # Act.
        result = instance.run()

        # Assert.
        self.assertEqual(2, result)

    @mock.patch.object(random, "randint", new=lambda *args: 7)
    def test_run_projective(self):
        # Arrange.
        # curve_params = shared.CurveParams(
        #     base_point=shared.CurveBasePoint(172235452673, 488838007757, 1),
        #     a=236367012452,
        #     b=74315650609,
        #     field_order=807368793739,
        #     curve_order=807369655039,
        # )
        curve_params = shared.CurveParams(
            base_point=shared.CurveBasePoint(2928, 42354, 1),
            a=40798,
            b=14047,
            field_order=62071,
            curve_order=62039,
        )
        projective.set_curve_params(curve_params)
        params = projective_rho.generate_params(curve_params)
        instance = projective_rho.EcProjectivePollardRhoDL(params)

        # Act.
        result = instance.run()

        # Assert.
        self.assertEqual(7, result)


if __name__ == "__main__":
    unittest.main()
