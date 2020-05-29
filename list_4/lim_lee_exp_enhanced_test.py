import random
import unittest

import lim_lee_exp_enhanced
import lookup_table_builder
import params_finder
import affine
import field
from affine import AffinePoint, set_curve_params
from shared import CurveBasePoint, CurveParams

AffinePoint = affine.AffinePoint
FieldInt = field.FieldInt


class LimLeeExpEnhancedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        curve_params = CurveParams(
            base_point=CurveBasePoint(172235452673, 488838007757),
            a=236367012452,
            b=74315650609,
            field_order=807368793739,
            curve_order=807369655039,
        )
        set_curve_params(curve_params)
        field.set_modulus(curve_params.field_order)
        params = (
            (256, 100),
            (256, 5000),
        )
        lookup_tables = {}
        g = AffinePoint(178539744208, 550836080620)

        for R_bits, S_max in params:
            a, b = lim_lee_exp_enhanced.optimize_parameters(R_bits=R_bits, S_max=S_max)
            lookup_tables[(R_bits, S_max)] = lim_lee_exp_enhanced.build_lookup_table(
                g, R_bits, a, b
            )

    def test_works_for_storage_size_R_bits_256_s_max_100(self):
        pass

    def test_works_for_storage_size_R_bits_256_s_max_500(self):
        pass


if __name__ == "__main__":
    unittest.main()
