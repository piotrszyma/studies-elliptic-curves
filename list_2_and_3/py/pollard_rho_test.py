import unittest
import unittest.mock as mock
import random

import pollard_rho_affine as affine_rho
import pollard_rho_projective as projective_rho

import projective
import affine


class TestRhoPollard(unittest.TestCase):
    
    @mock.patch.object(random, "randint", new=lambda *args: 2)
    def test_run_affine(self):
        # Arrange.
        curve_params = affine.CurveParams(
            base_point=affine.CurveBasePoint(172235452673, 488838007757),
            a=236367012452,
            b=74315650609,
            field_order=807368793739,
            curve_order=807369655039,
        )
        affine.set_curve_params(curve_params)
        params = affine_rho.generate_params(curve_params)
        instance = affine_rho.EcAffinePollardRhoDL(params)
        # import pdb
        # pdb.set_trace()

        # Act.
        result = instance.run()

        # Assert.
        self.assertEqual(2, result)


    @mock.patch.object(random, "randint", new=lambda *args: 2)
    def test_run_projective(self):
        # Arrange.
        # curve_params = projective.CurveParams(
        #     base_point=projective.CurveBasePoint(172235452673, 488838007757, 1),
        #     a=236367012452,
        #     b=74315650609,
        #     field_order=807368793739,
        #     curve_order=807369655039,
        # )
        curve_params = projective.CurveParams(
            base_point=projective.CurveBasePoint(2928, 42354, 1),
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
        self.assertEqual(2, result)



if __name__ == "__main__":
    unittest.main()
