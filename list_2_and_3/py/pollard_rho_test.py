import unittest
import unittest.mock as mock
import random

import pollard_rho

from affine import CurveBasePoint, CurveParams


class TestRhoPollard(unittest.TestCase):
    @mock.patch.object(random, "randint", new=lambda *args: 2)
    def test_run(self):
        # Arrange.
        curve_params = CurveParams(
            base_point=CurveBasePoint(172235452673, 488838007757),
            a=236367012452,
            b=74315650609,
            field_order=807368793739,
            curve_order=807369655039,
        )
        params = pollard_rho.generate_params(curve_params)
        instance = pollard_rho.EcAffinePollardRhoDL(params)

        # Act.
        result = instance.run()

        # Assert.
        self.assertEqual(2, result)


if __name__ == "__main__":
    unittest.main()
